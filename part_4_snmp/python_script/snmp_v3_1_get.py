#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pysnmp.hlapi import (
    SnmpEngine,
    UdpTransportTarget,
    UsmUserData,
    # 认证协议（Auth Protocol）
    usmNoAuthProtocol,            # 无认证（noAuth）
    usmHMACMD5AuthProtocol,       # HMAC-MD5-96认证算法
    usmHMACSHAAuthProtocol,       # HMAC-SHA-96认证算法
    usmHMAC128SHA224AuthProtocol, # HMAC-SHA-224认证算法
    usmHMAC192SHA256AuthProtocol, # HMAC-SHA-256认证算法
    usmHMAC256SHA384AuthProtocol, # HMAC-SHA-384认证算法
    usmHMAC384SHA512AuthProtocol, # HMAC-SHA-512认证算法

    # 加密协议（Priv Protocol）
    usmNoPrivProtocol,  # 无加密（noPriv）
    usmDESPrivProtocol,  # DES加密算法
    usm3DESEDEPrivProtocol,  # 3DES-EDE加密算法
    usmAesCfb128Protocol,  # AES-128加密算法（标准AES）
    usmAesCfb192Protocol,  # AES-192加密算法
    usmAesCfb256Protocol,  # AES-256加密算法
    usmAesBlumenthalCfb192Protocol,  # AES-192加密算法（Blumenthal旧标准）
    usmAesBlumenthalCfb256Protocol,  # AES-256加密算法（Blumenthal旧标准）
    usmAesCfb128Protocol,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd
)


def snmpv3_get(ip,
               oid,
               user,
               auth_key,
               priv_key,
               auth_protocol=usmHMACSHAAuthProtocol,
               priv_protocol=usmAesCfb128Protocol,
               port=161):
    # 创建SNMPv3会话
    engine = SnmpEngine()
    user_data = UsmUserData(
        userName=user,
        authKey=auth_key,
        privKey=priv_key,
        authProtocol=auth_protocol,    # 使用SHA认证
        privProtocol=priv_protocol       # 使用AES-128加密
    )

    # 执行GET请求
    g = getCmd(
        engine,
        user_data,
        UdpTransportTarget((ip, port), timeout=2, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(g)

    if errorIndication:
        print("获取失败: ", errorIndication)
    elif errorStatus:
        print("SNMP错误: %s at %s" % (errorStatus.prettyPrint(),
                                     errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
    else:
        for varBind in varBinds:
            return varBind[1].prettyPrint()


if __name__ == "__main__":
    # 请将以下参数替换为你的实际信息
    target_host = '10.1.1.254'  # 目标网络设备的IP地址
    target_port = 161  # 目标网络设备的SNMP端口，一般为161
    snmp_user = 'qytanguser'  # SNMPv3的用户名
    auth_key = 'Qytang.com'  # SNMPv3的认证密码
    priv_key = 'Qytang.com'  # SNMPv3的加密密码
    snmp_oid = "1.3.6.1.2.1.1.1.0"  # 系统描述
    # snmp_oid = "1.3.6.1.2.1.1.5.0"  # 系统名称
    # snmp_oid = "1.3.6.1.4.1.2011.6.3.4.1.2.1.1.0"  # CPU利用率
    # snmp_oid = '1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7.16842753'  # 内存利用率
    print(snmpv3_get(
        ip=target_host,
        oid=snmp_oid,
        user=snmp_user,
        auth_key=auth_key,
        priv_key=priv_key
    ))
