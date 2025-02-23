#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
# 将snmpv2_getbulk替换为snmpv3_getbulk
from snmp_v3_3_getbulk import snmpv3_getbulk


def snmpv3_set(ip, user, auth_key, priv_key, oid, value, port=161,
               auth_protocol=None, priv_protocol=None):
    # 如果未指定auth_protocol和priv_protocol，则使用默认SHA和AES-128
    if auth_protocol is None:
        auth_protocol = cmdgen.usmHMACSHAAuthProtocol
    if priv_protocol is None:
        priv_protocol = cmdgen.usmAesCfb128Protocol

    cmd_gen = cmdgen.CommandGenerator()

    # 根据value类型决定使用的类型编码
    if isinstance(value, str):
        set_value = rfc1902.OctetString(value)
    elif isinstance(value, int):
        set_value = rfc1902.Integer(value)
    else:
        raise ValueError("不支持的类型，请使用int或str类型的值。")

    error_indication, error_status, error_index, var_binds = cmd_gen.setCmd(
        cmdgen.UsmUserData(
            userName=user,
            authKey=auth_key,
            privKey=priv_key,
            authProtocol=auth_protocol,
            privProtocol=priv_protocol
        ),
        cmdgen.UdpTransportTarget((ip, port)),
        (oid, set_value)
    )

    # 错误处理
    if error_indication:
        print("写入错误!!!")
        print(error_indication)
    elif error_status:
        print("写入错误!!!")
        print('%s at %s' % (
            error_status.prettyPrint(),
            error_index and var_binds[int(error_index) - 1][0] or '?'
        ))
    else:
        print("写入成功!!!")

    for name, val in var_binds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


def get_if_oid(ip, user, auth_key, priv_key, if_name, port=161,
               auth_protocol=None, priv_protocol=None):
    """
    使用snmpv3_getbulk获取接口列表，然后根据接口名称找到对应的ifIndex，并构造ifAdminStatus的OID。
    """
    # 获取接口名称列表，对应OID为1.3.6.1.2.1.2.2.1.2
    if_result = snmpv3_getbulk(ip=ip,
                               user=user,
                               auth_key=auth_key,
                               priv_key=priv_key,
                               oid="1.3.6.1.2.1.2.2.1.2",
                               port=port,
                               auth_protocol=auth_protocol,
                               priv_protocol=priv_protocol,
                               non_repeat=0,
                               max_repeat=25)

    if_result_dict = {}
    for x, y in if_result:
        if_result_dict.update({y: x})

    # 与v2逻辑相同，通过名字找到对应的OID，然后把.2结尾替换成.7以获取ifAdminStatus OID
    if_oid = if_result_dict.get(if_name)
    if if_oid is None:
        raise ValueError("未找到名为%s的接口。" % if_name)

    # OID转换逻辑
    # 原始OID类似：SNMPv2-SMI::mib-2.2.2.1.2.10 需要替换为1.3.6.1.2.1.2.2.1.7.10
    # 先将SNMPv2-SMI::mib-2.2.2.1.2... 替换为数字OID
    numeric_oid = if_oid.replace('SNMPv2-SMI::mib-2.2.2.1.2', '1.3.6.1.2.1.2.2.1.2')
    # 接着替换最后的.2.为.7.
    if_oid_final = numeric_oid.replace('.2.', '.7.')
    return if_oid_final


# 1 为up , 2 为down
def shutdown_if(ip, user, auth_key, priv_key, if_name, op=1, port=161,
                auth_protocol=None, priv_protocol=None):
    no_shutdown_oid = get_if_oid(ip, user, auth_key, priv_key, if_name, port,
                                 auth_protocol=auth_protocol, priv_protocol=priv_protocol)
    snmpv3_set(ip, user, auth_key, priv_key, no_shutdown_oid, op, port=port,
               auth_protocol=auth_protocol, priv_protocol=priv_protocol)


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器

    ip_address = "10.1.1.254"
    # SNMPv3参数请根据实际设备修改
    snmp_user = "qytanguser"
    auth_key = "Qytang.com"
    priv_key = "Qytang.com"
    auth_protocol = cmdgen.usmHMACSHAAuthProtocol
    priv_protocol = cmdgen.usmAesCfb128Protocol

    # 设置主机名（通过SNMPv3的SET操作）
    snmpv3_set(ip_address, snmp_user, auth_key, priv_key, "1.3.6.1.2.1.1.5.0", "SW_L3-1", port=161,
               auth_protocol=auth_protocol, priv_protocol=priv_protocol)

    # 修改接口状态，如果是环回接口或其他接口，1为up, 2为down
    # 示例：ifIndex=10的接口
    snmpv3_set(ip_address, snmp_user, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.7.10", 1, port=161,
               auth_protocol=auth_protocol, priv_protocol=priv_protocol)

    # 根据接口名称up/down接口
    shutdown_if(ip_address, snmp_user, auth_key, priv_key, "10GE1/0/5", op=1, port=161,
                auth_protocol=auth_protocol, priv_protocol=priv_protocol)
