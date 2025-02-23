import json
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import ListAppTableRecordRequest
from huawei_1_netmiko.feishu_sdk.basic_info import app_id, app_secret


def find_record_id_by_username(app_token: str, table_id: str, username: str) -> str:
    """
    通过遍历记录，找到 "用户名" = username 的那一行的 record_id。
    若找不到则返回 None。
    """
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .build()

    # 一次最多拉取 page_size 条记录
    req = ListAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .page_size(100) \
        .build()

    resp = client.bitable.v1.app_table_record.list(req)
    if not resp.success():
        raise Exception(f"查询记录失败, code: {resp.code}, msg: {resp.msg}")

    records = resp.data.items
    has_more = getattr(resp.data, "has_more", False)
    page_token = getattr(resp.data, "page_token", None)

    # 分页
    while has_more and page_token:
        req.page_token(page_token)
        resp = client.bitable.v1.app_table_record.list(req)
        if not resp.success():
            raise Exception(f"查询记录失败, code: {resp.code}, msg: {resp.msg}")
        records.extend(resp.data.items)
        has_more = getattr(resp.data, "has_more", False)
        page_token = getattr(resp.data, "page_token", None)

    # 遍历查找 "用户名" = username 的行
    for r in records:
        # print(r.fields)
        if r.fields.get("username") == username:
            return r.record_id

    return None


if __name__ == "__main__":
    my_app_token = "TuSUbUniEaccHlsU387cPQgEndT"   # 替换为真实 base token
    my_table_id  = "tblA9FbAfKGRqyb0"             # 替换为真实 table_id
    record_id = find_record_id_by_username(my_app_token, my_table_id, "qytang-user12")
    print(f"找到 record_id = {record_id}")
