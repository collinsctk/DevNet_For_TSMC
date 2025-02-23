import pandas as pd
from pprint import pprint
from huawei_1_netmiko.excel_tools.excel_opts_1_create import excel_dir, excel_file_path

# 保存到新的 Excel 文件
excel_file_with_cmd = f'{excel_dir}users_with_cmds.xlsx'  # 输出文件名


# 生成命令的函数
def generate_cmd(row):
    # 根据 Excel 行数据生成命令
    cmds = []

    # 最后前面加上 aaa
    cmds.append("aaa")

    # ---使用excel的数据,拼接命令---
    cmds.append(f"undo local-user {row['username']}")
    cmds.append(f"local-user {row['username']} password irreversible-cipher {row['password']}")
    cmds.append(f"local-user {row['username']} level {row['priv']}")
    cmds.append(f"local-user {row['username']} service-type {row['services']}")

    # 最后加上 commit
    cmds.append("commit")

    return "\n".join(cmds)


def excel_insert(excel_file):
    # 读取 Excel 文件
    df = pd.read_excel(excel_file)

    # 转换DataFrame的每一行到字典
    # orient='records'表示每个字典代表一行，键是列名
    list_of_dicts = df.to_dict(orient='records')
    # pprint(list_of_dicts)
    """
    [{'password': 'Huawei@123',
      'priv': 3,
      'services': 'telnet ssh',
      'username': 'qytang-user11'},
     {'password': 'Huawei@123',
      'priv': 3,
      'services': 'http ssh',
      'username': 'qytang-user12'},
     {'password': 'Huawei@123',
      'priv': 3,
      'services': 'ssh',
      'username': 'qytang-user13'}]
    """
    # 应用生成命令的函数"generate_cmd", 从每一行读取数据, 产生新的一列"cmds"
    # axis=0：表示沿着列（垂直方向）进行操作，也就是按行（row-wise）进行计算或操作。
    # axis=1：表示沿着行（水平方向）进行操作，也就是按列（column-wise）进行计算或操作。
    df['cmds'] = df.apply(generate_cmd, axis=1)

    # 创建并写入excel
    df.to_excel(excel_file_with_cmd, index=False)

    print(f"命令已写入新文件：{excel_file_with_cmd}")


if __name__ == '__main__':
    excel_insert(excel_file_path)
