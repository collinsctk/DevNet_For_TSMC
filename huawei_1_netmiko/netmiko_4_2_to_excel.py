from huawei_1_netmiko.netmiko_2_ntc_template_1_basic import netmiko_ntc_template
from huawei_1_netmiko.netmiko_1_show_client import device_ip, username, password
from huawei_1_netmiko.excel_tools.excel_opts_2_insert import excel_dir
import pandas as pd
from pprint import pprint


def display_to_excel(excel_file):
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
    # 创建 DataFrame
    df = pd.DataFrame(users_result)
    # print(df)
    """
            username  ...    services
    0         qytang  ...         ssh
    1   qytang-user1  ...  telnet ssh
    2   qytang-user2  ...  telnet ssh
    3   qytang-user3  ...  telnet ssh
    4   qytang-user4  ...  telnet ssh
    5   qytang-user5  ...  telnet ssh
    6   qytang-user6  ...  telnet ssh
    7  qytang-user11  ...  telnet ssh
    8  qytang-user12  ...    ssh http
    9  qytang-user13  ...         ssh
    """
    # 将 'level' 列重命名为 'priv' 列
    df.rename(columns={'level': 'priv'}, inplace=True)

    # 保存到 Excel 文件
    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"数据已成功保存到 {excel_file}")


if __name__ == "__main__":
    excel_file_name = f'{excel_dir}users_from_device.xlsx'
    display_to_excel(excel_file_name)
