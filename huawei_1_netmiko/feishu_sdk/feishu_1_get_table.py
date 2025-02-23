# pip3.11 install lark-oapi
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import ListAppTableRequest, ListAppTableRecordRequest
from huawei_1_netmiko.feishu_sdk.basic_info import app_id, app_secret
from huawei_1_netmiko.feishu_sdk.tools_1_get_table_id import get_table_id


def list_table_records_by_name(app_token: str, table_name: str) -> list:
    """
    给定多维表格 app_token 和表的「人类可读名称 table_name」，返回该表中所有“非空行”的记录字段。
    """
    # ~~~~~~~开启debug 日志，方便排查问题~~~~~~~~~~~~~
    # client = lark.Client.builder() \
    #     .app_id(app_id) \
    #     .app_secret(app_secret) \
    #     .log_level(lark.LogLevel.DEBUG) \
    #     .build()

    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .build()

    found_table_id = get_table_id(app_token, table_name)

    # 2. 根据 table_id 拉取该表所有记录
    req_record = ListAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(found_table_id) \
        .page_size(100) \
        .build()

    resp_record = client.bitable.v1.app_table_record.list(req_record)
    if not resp_record.success():
        raise Exception(f"获取记录失败，code: {resp_record.code}, msg: {resp_record.msg}")

    records = resp_record.data.items
    has_more = getattr(resp_record.data, "has_more", False)
    page_token = getattr(resp_record.data, "page_token", None)

    # 分页循环
    while has_more and page_token:
        req_record.page_token(page_token)
        resp_record = client.bitable.v1.app_table_record.list(req_record)
        if not resp_record.success():
            raise Exception(f"获取记录失败，code: {resp_record.code}, msg: {resp_record.msg}")

        records.extend(resp_record.data.items)
        has_more = getattr(resp_record.data, "has_more", False)
        page_token = getattr(resp_record.data, "page_token", None)

    # 3. 过滤空记录，只保留有 fields 的行
    filtered_data = []
    for record in records:
        if record.fields:
            filtered_data.append(record.fields)

    return filtered_data


if __name__ == "__main__":
    from pprint import pprint
    # 你的 app_token（多维表格 Base token）和表的名称
    my_app_token = "TuSUbUniEaccHlsU387cPQgEndT"
    my_table_name = "qytang-table"
    pprint(list_table_records_by_name(my_app_token, my_table_name))
