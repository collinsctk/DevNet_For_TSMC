# pip3.11 install lark-oapi
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import UpdateAppTableRecordRequest
from lark_oapi.api.bitable.v1.model import AppTableRecord
from basic_info import app_id, app_secret
from huawei_1_netmiko.feishu_sdk.tools_1_get_table_id import get_table_id
from huawei_1_netmiko.feishu_sdk.tools_2_find_record_id import find_record_id_by_username


def update_services_field(app_token: str, table_name: str, username: str, update_fields: dict):
    # 创建client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .build()
    table_id = get_table_id(app_token, table_name)
    record_id = find_record_id_by_username(app_token, table_id, username)
    # 构造请求对象
    request = UpdateAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .record_id(record_id) \
        .request_body(
            AppTableRecord.builder()
            .fields(update_fields)
            .build()
        ) \
        .build()

    response = client.bitable.v1.app_table_record.update(request)
    if not response.success():
        raise Exception(f"更新记录失败, code: {response.code}, msg: {response.msg}")

    print("更新成功：", response.data.record.fields)


if __name__ == "__main__":
    # 如果你已经知道 record_id，可直接写死
    my_app_token = "TuSUbUniEaccHlsU387cPQgEndT"  # 替换
    my_table_name = "qytang-table"
    update_fields = {
        "services": ["ssh", "telnet"],
        "password": "Cisc0123"
    }
    update_services_field(
        app_token=my_app_token,
        table_name=my_table_name,
        username="qytang-user12",
        update_fields=update_fields
    )
