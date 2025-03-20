"""
    lager.artifact.commands

    Artifact upload and download commands
"""
import click
import boto3
import time
import json
import os
from pathlib import Path
from botocore.exceptions import ClientError
from ..context import get_default_gateway

# AWS Clients
iam_client = boto3.client("iam")
s3_client = None  # Will be initialized dynamically

def get_s3_client():
    """
    Returns an S3 client using dynamically generated access keys.
    If credentials are missing, they are loaded from ~/.lager_env.
    """
    env_file = os.path.expanduser("~/.lager_env")

    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY") or not os.getenv("AWS_S3_BUCKET"):
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
        else:
            click.echo("Error: AWS credentials or bucket name are missing. Run 'create-user' first.", err=True)
            exit(1)

    return boto3.client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    ), os.getenv("AWS_S3_BUCKET")

@click.group(name='artifact')
def _artifact():
    """
        Lager artifact commands
    """
    pass

@_artifact.command(name="create-user")
@click.argument("customer_id")
@click.pass_context
def create_user(ctx, customer_id):
    """
    Create an IAM user, generate access keys, create a unique S3 bucket, and attach S3 permissions.
    """
    try:
        username = f"customer-{customer_id}"
        bucket_name = f"lager-user-{customer_id}".lower().replace("_", "-")
        aws_region = "us-east-1"

        # Create IAM user
        user = iam_client.create_user(UserName=username)

        # Create S3 bucket for the user
        s3 = boto3.client("s3")
        try:
            if aws_region == "us-east-1":
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": aws_region}
                )
            click.echo(f"S3 bucket {bucket_name} created successfully.")
        except ClientError as e:
            click.echo(f"Error creating S3 bucket: {str(e)}", err=True)
            ctx.exit(1)

        # Create and attach policy for this specific bucket
        policy_arn = create_s3_access_policy(username, bucket_name)
        iam_client.attach_user_policy(UserName=username, PolicyArn=policy_arn)

        # Generate access keys
        try:
            keys = iam_client.create_access_key(UserName=username)
            access_key = keys["AccessKey"]["AccessKeyId"]
            secret_key = keys["AccessKey"]["SecretAccessKey"]
        except ClientError as e:
            click.echo(f"Error creating access key: {str(e)}", err=True)
            ctx.exit(1)

        # Save credentials to a .env file
        env_file = os.path.expanduser("~/.lager_env")
        with open(env_file, "w") as f:
            f.write(f"AWS_ACCESS_KEY_ID={access_key}\n")
            f.write(f"AWS_SECRET_ACCESS_KEY={secret_key}\n")
            f.write(f"AWS_S3_BUCKET={bucket_name}\n")

        click.echo(f"User {username} created successfully with S3 bucket: {bucket_name}")
        click.echo(f"Credentials saved to {env_file}. Run 'source {env_file}' to load them.")

    except Exception as e:
        click.echo(f"Error creating IAM user: {str(e)}", err=True)
        ctx.exit(1)

def create_s3_access_policy(username, bucket_name):
    """
    Create an IAM policy that grants S3 access to a specific user bucket.
    """
    policy_name = f"S3AccessPolicy-{username}"

    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:ListBucket"],
                "Resource": [f"arn:aws:s3:::{bucket_name}"]
            },
            {
                "Effect": "Allow",
                "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
                "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
            }
        ]
    }

    try:
        policy_response = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        return policy_response["Policy"]["Arn"]

    except ClientError as e:
        if e.response["Error"]["Code"] == "AccessDenied":
            click.echo(
                "Error: Missing 'iam:CreatePolicy' permission. "
                "Ensure your IAM user has the necessary policy permissions.",
                err=True
            )
            exit(1)
        else:
            click.echo(f"Error creating IAM policy: {str(e)}", err=True)
            exit(1)

@_artifact.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--remote-name', '-n', help='Name to save as in S3 (defaults to local filename)')
@click.pass_context
def upload(ctx, filepath, remote_name):
    """
    Upload a local file to the user's S3 bucket.
    """
    global s3_client
    s3_client, bucket_name = get_s3_client()

    try:
        path = Path(filepath)
        remote_name = remote_name or path.name
        file_key = f"uploads/{remote_name}"

        with open(filepath, 'rb') as file:
            s3_client.upload_fileobj(file, bucket_name, file_key)

        s3_url = f"https://{bucket_name}.s3.us-east-1.amazonaws.com/{file_key}"
        click.echo(f"Successfully uploaded {filepath} to {s3_url}")

    except Exception as e:
        click.echo(f"Error uploading file: {str(e)}", err=True)
        ctx.exit(1)

@_artifact.command()
@click.argument("filename")
@click.option("--output", "-o", type=click.Path(), help="Output path (defaults to current directory)")
@click.pass_context
def download(ctx, filename, output):
    """
    Download a remote file from the user's S3 bucket to local system.
    If the file is not immediately found, it will retry for up to 15 seconds before failing.
    """
    global s3_client
    s3_client, bucket_name = get_s3_client()

    file_key = f"uploads/{filename}"
    
    if output:
        output_path = Path(output)
        if output_path.is_dir():  # Append filename if only directory is provided
            output_path = output_path / filename
    else:
        output_path = Path.cwd() / filename  # Save to current directory if no output specified

    max_attempts = 15 
    wait_time = 1

    for attempt in range(1, max_attempts + 1):
        try:
            # Check if the file exists in S3
            s3_client.head_object(Bucket=bucket_name, Key=file_key)

            # File found, proceed with download
            with open(output_path, "wb") as file:
                s3_client.download_fileobj(bucket_name, file_key, file)

            click.echo(f"Successfully downloaded {filename} to {output_path}")
            return  # Exit function successfully

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                click.echo(f"File not found, attempt {attempt}/{max_attempts}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                click.echo(f"Error downloading file: {str(e)}", err=True)
                ctx.exit(1)

    click.echo(f"Error: File not found after {max_attempts} attempts. Check if the file exists in S3.", err=True)
    ctx.exit(1)


@_artifact.command()
@click.pass_context
def list(ctx):
    """
    List all artifacts in the user's S3 bucket.
    """
    global s3_client
    s3_client, bucket_name = get_s3_client()

    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='uploads/')

        if 'Contents' not in response:
            click.echo("No artifacts found")
            return

        for obj in response['Contents']:
            size_mb = obj['Size'] / (1024 * 1024)
            click.echo(f"{obj['Key']} ({size_mb:.2f} MB)")

    except Exception as e:
        click.echo(f"Error listing files: {str(e)}", err=True)
        ctx.exit(1)


@_artifact.command()
@click.argument('filename')
@click.pass_context
def delete(ctx, filename):
    """
    Delete a file from the user's S3 bucket.
    """
    global s3_client
    s3_client, bucket_name = get_s3_client()

    file_key = f'uploads/{filename}'

    try:
        # Check if file exists
        s3_client.head_object(Bucket=bucket_name, Key=file_key)

        # Delete file
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        click.echo(f"Successfully deleted {file_key} from S3.")

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            click.echo(f"Error: File '{file_key}' not found in S3.", err=True)
        else:
            click.echo(f"Error deleting file: {str(e)}", err=True)
        ctx.exit(1)