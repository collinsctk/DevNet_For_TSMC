import os
from part_1_netmiko.netmiko_1_show_client import netmiko_show_cred
from part_1_netmiko.netmiko_2_ntc_template_1_basic import clitable_to_dict
from textfsm import clitable
import yaml
from pprint import pprint


# 协程相关
import asyncio
import os


# 协程任务循环
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def async_netmiko_ntc_template(ip, username, password, cmd, device_type, ssh_port=22):

    ssh_ouput = netmiko_show_cred(ip, username, password, cmd, device_type, ssh_port=ssh_port)

    cli_table = clitable.CliTable('index', f'.{os.sep}ntc-template')

    attributes = {'Command': cmd, 'Vendor': device_type}

    cli_table.ParseCmd(ssh_ouput, attributes)

    parse_result = clitable_to_dict(cli_table)
    return {'device_ip': ip,
            'display_cmd': cmd,
            'display_result': parse_result}

tasks = []

display_devices_info_dir = './display-devices-info'
display_devices_info_file_name = 'display_devices.yml'


with open(f'{display_devices_info_dir}{os.sep}{display_devices_info_file_name}') as data_f:
    devices_info = yaml.safe_load(data_f.read())
    # pprint(devices_info)
    for device_info in devices_info:
        # 产生携程任务
        device_ip = device_info.get('device_ip')
        device_type = device_info.get('device_type')
        username = device_info.get('username')
        password = device_info.get('password')
        display_cmds = device_info.get('display_cmds')
        for display_cmd in display_cmds:
            task = loop.create_task(
                async_netmiko_ntc_template(device_ip, username, password, display_cmd, device_type))
            # 把产生的携程任务放入任务列表
            tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))

for t in tasks:
    result_list = []
    pprint(t.result())
    result_list.append(t.result())



