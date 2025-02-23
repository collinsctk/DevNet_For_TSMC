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
# pysnmp==4.4.12 现在是最新的7.1.16
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


async def snmpv2_get(ip, community, oid, port=161):
    # 使用 get_cmd 执行 SNMP GET 操作
    error_indication, error_status, error_index, var_binds = await get_cmd(
        SnmpEngine(),
        CommunityData(community),  # 配置 community
        await UdpTransportTarget.create((ip, port)),  # 配置目的地址和端口号
        ContextData(),
        ObjectType(ObjectIdentity(oid))  # 读取的 OID
    )

    # 错误处理
    if error_indication:
        print(error_indication)
    elif error_status:
        print(f'{error_status} at {error_index and var_binds[int(error_index) - 1][0] or "?"}')
    else:
        # 如果返回结果有多行，需要拼接后返回
        result_str = "".join([varBind.prettyPrint() for varBind in var_binds])
        # 返回的为一个元组，OID 与字符串结果
        return result_str.split("=")[0].strip(), result_str.split("=")[1].strip()

if __name__ == "__main__":
    # ip 地址与 snmp community 字符串
    ip_address = "196.21.5.211"
    community = "qytangro"

    # 使用 asyncio 运行异步函数
    result = asyncio.run(snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.1.0", port=161))
    if result:
        print(result)