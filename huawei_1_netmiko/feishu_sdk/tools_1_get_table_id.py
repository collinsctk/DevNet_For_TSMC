#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import ListAppTableRequest, ListAppTableRecordRequest
from huawei_1_netmiko.feishu_sdk.basic_info import app_id, app_secret


def get_table_id(app_token: str, table_name: str):
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .build()
    # 1. 根据 table_name 找到 table_id
    req_table = ListAppTableRequest.builder() \
        .app_token(app_token) \
        .page_size(50) \
        .build()
    resp_table = client.bitable.v1.app_table.list(req_table)
    if not resp_table.success():
        raise Exception(f"列出表失败，code: {resp_table.code}, msg: {resp_table.msg}")

    found_table_id = None
    for tbl in resp_table.data.items:
        if tbl.name == table_name:
            found_table_id = tbl.table_id
            break
    if not found_table_id:
        raise Exception(f"在 Base [{app_token}] 下，没有找到名为 [{table_name}] 的表")

    return found_table_id


if __name__ == '__main__':
    my_app_token = "TuSUbUniEaccHlsU387cPQgEndT"
    my_table_name = "qytang-table"
    print(get_table_id(my_app_token, my_table_name))
