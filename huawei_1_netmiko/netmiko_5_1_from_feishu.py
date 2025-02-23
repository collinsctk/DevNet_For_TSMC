from huawei_1_netmiko.netmiko_1_show_client import device_ip, username, password
from huawei_1_netmiko.netmiko_3_config_1_basic import netmiko_config_cred
from huawei_1_netmiko.feishu_sdk.feishu_1_get_table import list_table_records_by_name
from huawei_1_netmiko.feishu_sdk.basic_info import my_app_token, my_table_name
from jinja2 import Template
import os

config_template_dir = './config-template'
template_file_name = f'users.jinja2'


def config_from_excel(app_token, table_name):
    user_list = list_table_records_by_name(app_token, table_name)
    # print((user_list))
    with open(f'{config_template_dir}{os.sep}{template_file_name}') as template_f:
        template = Template(template_f.read())
        config_str = template.render(users=user_list)
        # print(config_str)
    cmds_list = config_str.split('\n')

    print(netmiko_config_cred(device_ip,
                              username,
                              password,
                              cmds_list,
                              'huawei_vrp',
                              verbose=True))


if __name__ == '__main__':
    config_from_excel(my_app_token, my_table_name)
