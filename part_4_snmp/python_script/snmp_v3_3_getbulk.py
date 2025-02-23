#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pysnmp.entity.rfc3413.oneliner import cmdgen


def snmpv3_getbulk(ip,
                   user,
                   auth_key,
                   priv_key,
                   oid,
                   auth_protocol=cmdgen.usmHMACSHAAuthProtocol,  # 使用SHA认证算法
                   priv_protocol=cmdgen.usmAesCfb128Protocol,    # 使用AES-128加密算法
                   port=161,
                   non_repeat=0,
                   max_repeat=10):
    """
    使用SNMPv3执行GetBulk请求（仅支持单个OID）。
    返回结果为列表，格式为[(oid, value), (oid, value), ...]。
    """

    cmdGen = cmdgen.CommandGenerator()

    # SNMPv3的用户数据：用户名、认证密钥、加密密钥
    # 根据需要修改auth_protocol和priv_protocol（例如usmHMACMD5AuthProtocol, usmDESPrivProtocol等）
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
        cmdgen.UsmUserData(
            userName=user,
            authKey=auth_key,
            privKey=priv_key,
            authProtocol=auth_protocol,
            privProtocol=priv_protocol
        ),
        cmdgen.UdpTransportTarget((ip, port)),
        non_repeat,
        max_repeat,
        oid
    )

    if errorIndication:
        print("获取失败:", errorIndication)
        return []
    elif errorStatus:
        print("SNMP错误: %s at %s" % (errorStatus.prettyPrint(),
                                  errorIndex and varBindTable[int(errorIndex)-1][0] or '?'))
        return []

    result = []
    # 按行解析返回结果的表格
    for varBindTableRow in varBindTable:
        for name, val in varBindTableRow:
            str_name = str(name)
            # 检查返回的OID是否仍在请求的OID子树下，如果超出子树，直接返回
            if not str_name.startswith(oid):
                return result
            result.append((str_name, str(val)))

    return result


if __name__ == "__main__":
    ip_address = "10.1.1.254"
    snmp_user = 'qytanguser'
    auth_key = 'Qytang.com'
    priv_key = 'Qytang.com'

    # 示例OID（接口描述）
    # snmp_oid = "1.3.6.1.2.1.2.2.1.2"  # 接口描述
    # snmp_oid = "1.3.6.1.2.1.2.2.1.5"  # 接口速率
    # snmp_oid = "1.3.6.1.2.1.2.2.1.10" # 进接口字节数
    snmp_oid = "1.3.6.1.2.1.2.2.1.16" # 出接口字节数
    raw_name_list = snmpv3_getbulk(
        ip_address,
        snmp_user,
        auth_key,
        priv_key,
        snmp_oid,
        auth_protocol=cmdgen.usmHMACSHAAuthProtocol,
        priv_protocol=cmdgen.usmAesCfb128Protocol,
        non_repeat=0,
        max_repeat=10
    )

    if_name_list = [val for _, val in raw_name_list]

    # 这里你可以像在v2中那样进一步处理数据，比如再获取ifSpeed, ifInOctets, ifOutOctets等，并组合
    print(if_name_list)
