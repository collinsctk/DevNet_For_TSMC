from huawei_1_netmiko.netmiko_2_ntc_template_1_basic import netmiko_ntc_template
from huawei_1_netmiko.netmiko_1_show_client import device_ip, username, password
from huawei_1_netmiko.feishu_sdk.feishu_4_add_table import create_table
from huawei_1_netmiko.feishu_sdk.feishu_3_insert_data import insert_records_into_table
from huawei_1_netmiko.feishu_sdk.basic_info import my_app_token, my_table_name


def display_to_feishu(table_name):
    users_result = (netmiko_ntc_template(device_ip,
                                         username,
                                         password,
                                         # -------专门为此做过ntc-template的解析------
                                         'display current-configuration | in user',
                                         'huawei_vrp'))
    # pprint(users_result)
    """
    [{'level': '3',
      'password': '$1c$5OQj722(cA$o](e(GQh2.N6@WG]PIYPlUQ16fG~l!=PpH@h/J,/$',
      'services': 'ssh',
      'username': 'qytang'},
     {'level': '3',
      'password': '$1c$FlFXJD7O6Q$xhb]34bG]=M!53$H$B{61qiR*~@:%4T0N>9c\\Rg+$',
      'services': 'telnet ssh',
      'username': 'qytang-user1'},
     {'level': '3',
      'password': '$1c$"5rrVY2ZOB$d9;\'0|MBpJ_v|[H-Pa=7V*^Y2UsQ,%,7}fD2n|Z#$',
      'services': 'telnet ssh',
      'username': 'qytang-user2'},
     {'level': '3',
      'password': '$1c$+q@^JDg#kN$W{l[Q}chHFD2j>5&rvEIaYP7O6Xs&W#})7ZX(OzY$',
      'services': 'telnet ssh',
      'username': 'qytang-user3'},
     {'level': '3',
      'password': '$1c$K{`=6=lVU1$@$iv-VrVrRZ|TWVM^a(,~WvX0z~eyAw:0RXw`)#4$',
      'services': 'telnet ssh',
      'username': 'qytang-user4'},
     {'level': '3',
      'password': '$1c$T|MHQ4u`GH$0ihOC}xmgD8ura2(h^=EV*_LI83__-Xy:2#)hG|&$',
      'services': 'telnet ssh',
      'username': 'qytang-user5'},
     {'level': '3',
      'password': '$1c$Eg(C,4*q"0$o|8y)Zvb$\'[&FaY-\\j>SfJoM6Z1KC5Id,&91B-XF$',
      'services': 'telnet ssh',
      'username': 'qytang-user6'},
     {'level': '3',
      'password': "$1c$=Uy_Mv'Rm8$w<{S5KsD&4dBUU5OuK`2'TW)%u:`5'^*g@0UAb|:$",
      'services': 'telnet ssh',
      'username': 'qytang-user11'},
     {'level': '3',
      'password': '$1c$h8QmIEHjHQ$W"u!%C}~1+vicR9;{wHT790_#i7**,kY$gQt#LXJ$',
      'services': 'ssh http',
      'username': 'qytang-user12'},
     {'level': '3',
      'password': '$1c$e0X|G=|:)$$zM5QM.O@+%|hTS9B96*!qC!!*5H[[2:R:)@g%Tf6$',
      'services': 'ssh',
      'username': 'qytang-user13'}]
      """
    users_insert = []
    for u in users_result:
        u['services'] = [s.strip() for s in u['services'].split()]
        u['priv'] = int(u.pop("level"))
        users_insert.append(u)
    create_table(my_app_token, table_name)
    insert_records_into_table(my_app_token, table_name, users_insert)


if __name__ == "__main__":
    from datetime import datetime
    table_name = f'用户备份表{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    display_to_feishu(table_name)
    # ~~~debug~~~~
    # client = lark.Client.builder() \
    #     .app_id(app_id) \
    #     .app_secret(app_secret) \
    #     .log_level(lark.LogLevel.DEBUG) \  ~~~注释掉就没有bug了
    #     .build()
