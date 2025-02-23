#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


from pysnmp.entity.rfc3413.oneliner import cmdgen


def snmpv2_getbulk(ip, community, oid, count=25, port=161):
    cmd_gen = cmdgen.CommandGenerator()

    error_indication, error_status, error_index, var_bind_table = cmd_gen.bulkCmd(
        cmdgen.CommunityData(community),  # 配置community
        cmdgen.UdpTransportTarget((ip, port)),  # 配置IP地址和端口号
        0, count,  # 0为non-repeaters 和  25为max-repetitions(一个数据包中最多25个条目，和显示无关)
        oid,  # OID
    )

    """
    non-repeaters介绍
    the number of objects that are only expected to return a single GETNEXT instance, not multiple instances. Managers \
    frequently request the value of sysUpTime and only want that instance plus a list of other objects.
    max-repetitions介绍
    the number of objects that should be returned for all the repeating OIDs. Agent's must truncate the list to \
    something shorter if it won't fit within the max-message size supported by the command generator or the agent.
    详细介绍
    https://www.webnms.com/snmp/help/snmpapi/snmpv3/snmp_operations/snmp_getbulk.html
    """
    # 错误处理
    if error_indication:
        print(error_indication)
    elif error_status:
        print(error_status)

    result = []
    # varBindTable是个list，元素的个数可能有好多个。它的元素也是list，这个list里的元素是ObjectType，个数只有1个。
    for var_bind_table_row in var_bind_table:
        for item in var_bind_table_row:
            result.append((item.prettyPrint().split("=")[0].strip(), item.prettyPrint().split("=")[1].strip()))
    return result


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    from pprint import pprint
    # ip地址与snmp community字符串
    ip_address = "10.1.1.254"
    community = "Qytang.com"

    # 接口名称
    raw_name_list = snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.2", port=161)
    if_name_list = [raw_if_name[1] for raw_if_name in raw_name_list]
    # print(if_name_list)

    # 接口速率
    raw_speed_list = snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.5", port=161)
    if_speed_list = [raw_speed[1] for raw_speed in raw_speed_list]
    # print(if_speed_list)

    # 进接口字节数
    raw_in_bytes_list = snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.10", port=161)
    if_in_bytes_list = [raw_in_bytes[1] for raw_in_bytes in raw_in_bytes_list]
    # print(if_in_bytes_list)

    # 出接口字节数
    raw_out_bytes_list = snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.16", port=161)
    if_out_bytes_list = [raw_out_bytes[1] for raw_out_bytes in raw_out_bytes_list]
    # print(if_out_bytes_list)

    interface_list = []
    for name, speed, in_bytes, out_bytes in zip(if_name_list, if_speed_list, if_in_bytes_list, if_out_bytes_list):
        interface_list.append({
            'interface_name': name,
            'interface_speed': speed,
            'in_bytes': in_bytes,
            'out_bytes': out_bytes
        })

    pprint(interface_list)