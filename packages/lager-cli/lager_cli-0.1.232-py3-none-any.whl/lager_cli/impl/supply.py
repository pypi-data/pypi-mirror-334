import os
import json
import time
from lager.pcb.net import Net, NetType
from lager.pcb.defines import Mode
from lager.pcb.device import DeviceError

def net_setup(*args, **kwargs):
    pass

def net_teardown(*args, **kwargs):
    pass

def set_voltage(target_net, value, ocp, ovp):
    if ocp != None:
        target_net.set_ocp(ocp)
    if ovp != None:
        target_net.set_ovp(ovp)

    if value != None:
        target_net.set_voltage(value)
        return

    print(f"Voltage: {target_net.voltage()}")

def set_current(target_net, value, ocp, ovp):
    if ocp != None:
        target_net.set_ocp(ocp)
    if ovp != None:
        target_net.set_ovp(ovp)  

    if value != None:
        target_net.set_current(value)
        return

    print(f"Current: {target_net.current()}")

def clear_ovp(target_net):
    try:
        target_net.clear_ovp()
    except DeviceError as exc:
        if b'OVP' in exc.args[0] or b'over voltage' in exc.args[0] or b'overvoltage' in exc.args[0]:
            target_net.clear_ovp()

def clear_ocp(target_net):
    try:
        target_net.clear_ocp()
    except DeviceError as exc:
        if b'OCP' in exc.args[0] or b'overcurrent' in exc.args[0]:
            target_net.clear_ocp()

def get_state(target_net):
    print(f"Voltage: {target_net.voltage()}")
    print(f"Current: {target_net.current()}")
    print(f"Power: {target_net.power()}")
    print(f"Over Current Limit {target_net.get_ocp_limit()}")
    print(f"    Net in Over Current: {target_net.is_ocp()}")
    print(f"Over Voltage Limit {target_net.get_ovp_limit()}")
    print(f"    Net in Over Voltage: {target_net.is_ovp()}")     


def disable_net(target_net):
    target_net.disable() 

def enable_net(target_net):
    target_net.enable() 

def set_supply_mode(target_net):
    target_net.set_mode(Mode.PowerSupply)


def main():
    command = json.loads(os.environ['LAGER_COMMAND_DATA'])
    netname = command['params'].pop('netname')
    target_net = Net(netname, type=NetType.PowerSupply, setup_function=net_setup, teardown_function=net_teardown)
    if command['action'] == 'voltage':
        set_voltage(target_net, **command['params'])
    elif command['action'] == 'current':
        set_current(target_net, **command['params'])
    elif command['action'] == 'get_state':
        get_state(target_net, **command['params'])
    elif command['action'] == 'disable_net':
        disable_net(target_net, **command['params'])
    elif command['action'] == 'enable_net': 
        enable_net(target_net, **command['params'])
    elif command['action'] == 'set_mode':
        set_supply_mode(target_net, **command['params'])
    elif command['action'] == 'clear_ovp':
        clear_ovp(target_net, **command['params'])
    elif command['action'] == 'clear_ocp':
        clear_ocp(target_net, **command['params'])
    else:
        pass

if __name__ == '__main__':
    main()
