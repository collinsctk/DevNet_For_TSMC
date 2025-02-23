from huawei_3_snmp.python_script.snmp_v2_1_get import snmpv2_get
from huawei_3_snmp.python_script.snmp_v2_3_getbulk import snmpv2_getbulk


def snmpv2_get_all(ip_address, community):
    # 主机名
    sys_name = snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.5.0", port=161)[1]

    # hwEntityCpuUsage
    # 实体实时的CPU使用率 取值范围：0～100 缺省值：0
    cpu_usage = int(snmpv2_get(ip_address, community, "1.3.6.1.4.1.2011.5.25.31.1.1.1.1.5.9", port=161)[1])

    # hwMemoryDevSize
    # 查询一个实体的内存总量，单位为字节(byte)。
    total = int(snmpv2_get(ip_address, community, "1.3.6.1.4.1.2011.6.3.5.1.1.2.0.0.0", port=161)[1])
    # hwMemoryDevFree
    # 查询一个实体空闲的内存总量，单位为字节(byte)。
    free = int(snmpv2_get(ip_address, community, "1.3.6.1.4.1.2011.6.3.5.1.1.3.0.0.0", port=161)[1])

    mem_percent = (round((total - free) / total, 4)) * 100

    # -----------------------------------------------------
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

    return {'device_ip': ip_address,
            'hostname': sys_name,
            'cpu_usage_percent': cpu_usage,
            'mem_usage_percent': mem_percent,
            'interface_list': interface_list
            }


if __name__ == "__main__":
    # pyasn1==0.4.8
    # pysnmp==4.4.12
    # 使用Linux解释器 & WIN解释器

    # ip地址与snmp community字符串
    from pprint import pprint
    ip_address = "10.1.1.254"
    community = "Qytang.com"
    pprint(snmpv2_get_all(ip_address, community))
