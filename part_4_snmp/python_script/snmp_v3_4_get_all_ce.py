#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snmp_v3_1_get import snmpv3_get
from snmp_v3_3_getbulk import snmpv3_getbulk


def snmpv3_get_all(ip_address, user, auth_key, priv_key,
                   auth_protocol=None,   # 可选，如usmHMACSHAAuthProtocol
                   priv_protocol=None,   # 可选，如usmAesCfb128Protocol
                   port=161):
    """
    使用SNMPv3获取设备信息，包括主机名、CPU使用率、内存使用率和接口相关信息。
    """

    # 如果未指定auth_protocol和priv_protocol，则使用默认SHA和AES-128
    if auth_protocol is None:
        from pysnmp.hlapi import usmHMACSHAAuthProtocol
        auth_protocol = usmHMACSHAAuthProtocol
    if priv_protocol is None:
        from pysnmp.hlapi import usmAesCfb128Protocol
        priv_protocol = usmAesCfb128Protocol

    # 主机名
    sys_name_oid = "1.3.6.1.2.1.1.5.0"
    sys_name = snmpv3_get(ip=ip_address,
                          oid=sys_name_oid,
                          user=user,
                          auth_key=auth_key,
                          priv_key=priv_key,
                          auth_protocol=auth_protocol,
                          priv_protocol=priv_protocol,
                          port=port)

    # CPU使用率 实体实时的CPU使用率: 1.3.6.1.4.1.2011.6.3.4.1.2.1.1.0
    cpu_usage_oid = "1.3.6.1.4.1.2011.6.3.4.1.2.1.1.0"
    cpu_usage_val = snmpv3_get(ip=ip_address,
                               oid=cpu_usage_oid,
                               user=user,
                               auth_key=auth_key,
                               priv_key=priv_key,
                               auth_protocol=auth_protocol,
                               priv_protocol=priv_protocol,
                               port=port)
    cpu_usage = int(cpu_usage_val) if cpu_usage_val is not None else 0

    # 内存使用率 OID: 1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7.16842753
    mem_percent_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7.16842753'
    mem_percent_val = snmpv3_get(ip=ip_address,
                                 oid=mem_percent_oid,
                                 user=user,
                                 auth_key=auth_key,
                                 priv_key=priv_key,
                                 auth_protocol=auth_protocol,
                                 priv_protocol=priv_protocol,
                                 port=port)
    mem_percent = int(mem_percent_val) if mem_percent_val is not None else 0

    # 获取接口相关信息（批量）
    oid_if_name      = "1.3.6.1.2.1.2.2.1.2"   # 接口名称
    oid_if_speed     = "1.3.6.1.2.1.2.2.1.5"   # 接口速率
    oid_if_in_octets = "1.3.6.1.2.1.2.2.1.10"  # 进接口字节数
    oid_if_out_octets= "1.3.6.1.2.1.2.2.1.16"  # 出接口字节数

    raw_name_list = snmpv3_getbulk(ip=ip_address,
                                   user=user,
                                   auth_key=auth_key,
                                   priv_key=priv_key,
                                   oid=oid_if_name,
                                   auth_protocol=auth_protocol,
                                   priv_protocol=priv_protocol,
                                   port=port,
                                   non_repeat=0,
                                   max_repeat=25)
    if_name_list = [val for _, val in raw_name_list]

    raw_speed_list = snmpv3_getbulk(ip=ip_address,
                                    user=user,
                                    auth_key=auth_key,
                                    priv_key=priv_key,
                                    oid=oid_if_speed,
                                    auth_protocol=auth_protocol,
                                    priv_protocol=priv_protocol,
                                    port=port,
                                    non_repeat=0,
                                    max_repeat=25)
    if_speed_list = [val for _, val in raw_speed_list]

    raw_in_bytes_list = snmpv3_getbulk(ip=ip_address,
                                       user=user,
                                       auth_key=auth_key,
                                       priv_key=priv_key,
                                       oid=oid_if_in_octets,
                                       auth_protocol=auth_protocol,
                                       priv_protocol=priv_protocol,
                                       port=port,
                                       non_repeat=0,
                                       max_repeat=25)
    if_in_bytes_list = [val for _, val in raw_in_bytes_list]

    raw_out_bytes_list = snmpv3_getbulk(ip=ip_address,
                                        user=user,
                                        auth_key=auth_key,
                                        priv_key=priv_key,
                                        oid=oid_if_out_octets,
                                        auth_protocol=auth_protocol,
                                        priv_protocol=priv_protocol,
                                        port=port,
                                        non_repeat=0,
                                        max_repeat=25)
    if_out_bytes_list = [val for _, val in raw_out_bytes_list]

    interface_list = []
    # 尝试对齐长度，避免因为缺少数据导致报错
    length = min(len(if_name_list), len(if_speed_list), len(if_in_bytes_list), len(if_out_bytes_list))
    for i in range(length):
        name = if_name_list[i]
        speed = if_speed_list[i]
        in_bytes = if_in_bytes_list[i]
        out_bytes = if_out_bytes_list[i]

        # 这里的判断逻辑同v2，只在in_bytes和out_bytes为整数，
        # 且不同时为0时添加
        if in_bytes.isdigit() and out_bytes.isdigit():
            in_val = int(in_bytes)
            out_val = int(out_bytes)
            # 如果进出流量都为0，则不加入列表
            if not (in_val == 0 and out_val == 0):
                interface_list.append({
                    'interface_name': name,
                    'interface_speed': speed,
                    'in_bytes': in_val,
                    'out_bytes': out_val
                })

    return {
        'device_ip': ip_address,
        'hostname': sys_name,
        'cpu_usage_percent': cpu_usage,
        'mem_usage_percent': mem_percent,
        'interface_list': interface_list
    }


if __name__ == "__main__":
    from pprint import pprint
    # 根据实际情况修改参数
    target_host = "10.1.1.254"
    snmp_user = "qytanguser"
    auth_key = "Qytang.com"
    priv_key = "Qytang.com"

    # 根据设备支持情况选择合适的协议，如需要可修改
    from pysnmp.hlapi import usmHMACSHAAuthProtocol, usmAesCfb128Protocol

    result = snmpv3_get_all(ip_address=target_host,
                            user=snmp_user,
                            auth_key=auth_key,
                            priv_key=priv_key,
                            auth_protocol=usmHMACSHAAuthProtocol,
                            priv_protocol=usmAesCfb128Protocol)
    pprint(result)
