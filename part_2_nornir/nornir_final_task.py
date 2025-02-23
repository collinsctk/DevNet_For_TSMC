from nornir import InitNornir
from nornir.core.task import Task, Result
from netmiko import Netmiko
# pip3 install nornir-netmiko
from nornir_netmiko.tasks import netmiko_send_command  # Netmiko发送exec命令(show命令)
from nornir_netmiko.tasks import netmiko_send_config  # Netmiko发送配置命令

# pip3 install nornir-jinja2
from nornir_jinja2.plugins.tasks import template_file   # Jinja2读取模板的Task

# pip3 install nornir-utils
from nornir_utils.plugins.functions import print_result
from vault.python_script.vault_1_init import client


# 加载配置文件config.yaml
nr = InitNornir(
    config_file="config.yaml",
    # dry_run=True
)

# 过滤出路由器
routers = nr.filter(
    type="router",
    # site='beijing'
)


# 模板目录
templates_path = './templates/'

# 从vault读取信息,并更新nornir inventory(写入认证用的用户名和密码)
for host in routers.inventory.hosts.keys():
    # routers.inventory.hosts 是如下字典
    # {'c8kv1': Host: c8kv1, 'c8kv2': Host: c8kv2}

    # routers.inventory.hosts.keys()
    # ['c8kv1', 'c8kv2']

    # 从vault读取用户名和密码
    vault_data = client.secrets.kv.v2.read_secret_version(
                    mount_point='qytang',
                    path=f'{nr.inventory.hosts[host].platform}/cred',
                    raise_on_deleted_version=True  # 显式设置参数为 True
                    )
    cred_data = vault_data['data']['data']
    # 更新nornir inventory对应host的用户名和密码
    # c8kv1:
    #     groups:
    #         - cisco_ios
    #     hostname: 10.10.1.1
    #     username: admin
    #     password: Cisc0123

    # 写入设备(<class 'nornir.core.inventory.Host'>)的username属性
    nr.inventory.hosts[host].username = cred_data.get('username')
    # 写入设备(<class 'nornir.core.inventory.Host'>)的password属性
    nr.inventory.hosts[host].password = cred_data.get('password')


def qyt_netmiko_send_command(task: Task, command_string: str) -> Result:
    device_info = {
                    'host': task.host.hostname,
                    'username': task.host.username,
                    'password': task.host.password,
                    'device_type': task.host.platform
    }
    try:
        net_connect = Netmiko(**device_info)
        return Result(
            host=task.host,
            result=net_connect.send_command(command_string, use_textfsm=True)
        )

    except Exception as e:
        print(f'connection error ip: {task.host.hostname} error: {str(e)}')


# 执行show命令
# 路由器show ip inter brief
netmiko_show_result = routers.run(
                                  # task=netmiko_send_command,
                                  task=qyt_netmiko_send_command,
                                  name='Nornir执行Show命令',
                                  command_string="show ip inter brie")
print_result(netmiko_show_result)


# 打印返回结果
for device_name in netmiko_show_result:
    print('-'*50 + 'start' + '-'*50)
    print(device_name)        # c8kv1
    print(type(device_name))  # <class 'str'>
    print('='*50 + device_name + '='*50)
    print(type(netmiko_show_result[device_name].result))  # <class 'str'>
    print(netmiko_show_result[device_name].result)        # show命令的完整结果
    print('-' * 50 + 'end' + '-' * 50)


# 配置路由器函数
def config_routers(task):
    # -------------------------------配置接口-------------------------
    # 读取模板,并且通过参数render为具体配置
    ios_interface_template = task.run(
        name='第一步.1:读取IOS接口配置模板',
        task=template_file,  # Jinja2读取模板的Task
        template='cisco_ios_interface.template',  # 模板名
        path=templates_path  # 模板目录
    )
    # print(ios_interface_template.result)  # 多行字符串
    # print(ios_interface_template.result.split('\n'))  # 列表， 包含每一行的命令
    # 传入具体配置, 对设备进行配置, 注意需要".split('\n')"把配置转换为列表, 默认结果为多行字符串
    task.run(task=netmiko_send_config,
             name='第一步.2:配置路由器接口',
             config_commands=ios_interface_template.result.split('\n'),  # 注意此处提取了上一步操作的结果
             cmd_verify=True)

    # -------------------------------配置OSPF-------------------------
    # 读取模板,并且通过参数render为具体配置
    ospf_template = task.run(
        task=template_file,  # Jinja2读取模板的Task
        name='第二步.1:读取路由器OSPF模板',
        template='cisco_ios_ospf.template',  # 模板名
        path=templates_path  # 模板目录
    )
    # 传入具体配置, 对设备进行配置, 注意需要".split('\n')"把配置转换为列表, 默认结果为多行字符串
    task.run(task=netmiko_send_config,
             name='第二步.2:配置路由器OSPF',
             config_commands=ospf_template.result.split('\n'),  # 注意此处提取了上一步操作的结果
             cmd_verify=True)

    # -------------------------------配置SNMP-------------------------
    # 读取模板,并且通过参数render为具体配置
    snmp_template = task.run(
        task=template_file,  # Jinja2读取模板的Task
        name='第三步.1:读取路由器SNMP模板',
        template='cisco_ios_snmp.template',  # 模板名
        path=templates_path  # 模板目录
    )
    # 传入具体配置, 对设备进行配置, 注意需要".split('\n')"把配置转换为列表, 默认结果为多行字符串
    task.run(task=netmiko_send_config,
             name='第三步.2:配置路由器SNMP',
             config_commands=snmp_template.result.split('\n'),  # 注意此处提取了上一步操作的结果
             cmd_verify=True)

    # -------------------------------配置Logging-------------------------
    # 读取模板,并且通过参数render为具体配置
    logging_template = task.run(
        task=template_file,  # Jinja2读取模板的Task
        name='第四步.1:读取路由器Logging模板',
        template='cisco_ios_logging.template',  # 模板名
        path=templates_path  # 模板目录
    )
    # 传入具体配置, 对设备进行配置, 注意需要".split('\n')"把配置转换为列表, 默认结果为多行字符串
    task.run(task=netmiko_send_config,
             name='第四步.2:配置路由器Logging',
             config_commands=logging_template.result.split('\n'),  # 注意此处提取了上一步操作的结果
             cmd_verify=True)


# 执行配置路由器并打印结果
run_result = routers.run(task=config_routers,
                         name='配置路由器',)
print_result(run_result)

