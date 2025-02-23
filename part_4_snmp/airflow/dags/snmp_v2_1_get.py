#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

# -----下面是解决win报错问题------
# ------Linux下视乎没有问题------
# pyasn1==0.4.8
# pysnmp==4.4.12
from pysnmp.hlapi import *


def snmpv2_get(ip, community, oid, port=161):
    # varBinds是列表，列表中的每个元素的类型是ObjectType（该类型的对象表示MIB variable）
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),  # 配置community
               UdpTransportTarget((ip, port)),  # 配置目的地址和端口号
               ContextData(),
               ObjectType(ObjectIdentity(oid))  # 读取的OID
               )
    )
    # 错误处理
    if error_indication:
        print(error_indication)
    elif error_status:
        print('%s at %s' % (
            error_status,
            error_index and var_binds[int(error_index) - 1][0] or '?'
        )
              )
    # 如果返回结果有多行,需要拼接后返回
    result = ""

    for varBind in var_binds:

        result = result + varBind.prettyPrint() # 返回结果！
    # 返回的为一个元组,OID与字符串结果
    # print(result)
    return result.split("=")[0].strip(), result.split("=")[1].strip()


if __name__ == "__main__":
    # pyasn1==0.4.8
    # pysnmp==4.4.12
    # 使用Linux解释器 & WIN解释器

    # ip地址与snmp community字符串
    ip_address = "10.1.1.254"
    community = "Qytang.com"
    # 华为OID查询
    # https://info.support.huawei.com/info-finder/tool/zh/enterprise/mib/
    # 使用snmpwalk测试, 需要在官方oid基础上继续向下找
    # snmpwalk -v 2c -c Qytang.com 10.1.1.254 1.3.6.1.4.1.2011.6.3.5.1.1.2

    # 系统描述
    sys_info = snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.1.0", port=161)[1]
    print(f'系统描述: {sys_info}')
    # 主机名
    sys_name = snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.5.0", port=161)[1]
    print(f'系统名称: {sys_name}')
    # hwEntityCpuUsage
    # 实体实时的CPU使用率 取值范围：0～100 缺省值：0
    # ------------------AR用-----------------------
    # cpu_oid = "1.3.6.1.4.1.2011.5.25.31.1.1.1.1.5.9"
    # ------------------CE用-----------------------
    cpu_oid = "1.3.6.1.4.1.2011.6.3.4.1.2.1.1.0"
    cpu_usage = int(snmpv2_get(ip_address, community, cpu_oid, port=161)[1])
    print(f'CPU利用率: {cpu_usage}%')
    # hwMemoryDevSize
    # 查询一个实体的内存总量，单位为字节(byte)。
    # ===================内存AR的方案====================
    # # ------------------AR用-----------------------
    # mem_total_oid = "1.3.6.1.4.1.2011.6.3.5.1.1.2.0.0.0"
    # total = int(snmpv2_get(ip_address, community, mem_total_oid, port=161)[1])
    # # hwMemoryDevFree
    # # 查询一个实体空闲的内存总量，单位为字节(byte)。
    # # ------------------AR用-----------------------
    # mem_free_oid = "1.3.6.1.4.1.2011.6.3.5.1.1.3.0.0.0"
    # free = int(snmpv2_get(ip_address, community, mem_free_oid, port=161)[1])
    #
    # percent = (round((total - free) / total, 4)) * 100
    # print(f'内存利用率: {percent}%')

    # ===================内存CE的方案====================
    mem_percent_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7.16842753'
    percent = int(snmpv2_get(ip_address, community, mem_percent_oid, port=161)[1])
    print(f'内存利用率: {percent}%')


