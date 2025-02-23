# pip3.11 install lark-oapi
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import BatchCreateAppTableRecordRequest, BatchCreateAppTableRecordRequestBody
from lark_oapi.api.bitable.v1.model import AppTableRecord
from huawei_1_netmiko.feishu_sdk.basic_info import app_id, app_secret
from huawei_1_netmiko.feishu_sdk.tools_1_get_table_id import get_table_id  # 你已有的函数


def insert_records_into_table(app_token: str, table_name: str, records_list: list[dict]):
    """
    给定多维表格 app_token、表的名称 table_name，
    以及一批待插入的记录(列表，每个元素是一个字段字典)，批量插入到该表中。
    """

    # 1. 创建 Lark Client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .build()

    # 2. 根据表名获取 table_id
    table_id = get_table_id(app_token, table_name)

    # 3. 构造批量插入请求体
    #    将每个记录 dict 转换为 AppTableRecord 对象并加入列表
    record_objects = []
    for rec in records_list:
        record_objects.append(
            AppTableRecord.builder().fields(rec).build()
        )

    request_body = BatchCreateAppTableRecordRequestBody.builder() \
        .records(record_objects) \
        .build()

    # 4. 发起批量插入请求
    request = BatchCreateAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .request_body(request_body) \
        .build()

    response = client.bitable.v1.app_table_record.batch_create(request)

    # 5. 检查结果
    if not response.success():
        raise Exception(f"插入记录失败, code: {response.code}, msg: {response.msg}")

    # 6. 打印插入成功后返回的记录信息
    print("批量插入成功，返回结果：", [r.fields for r in response.data.records])


if __name__ == "__main__":
    # 示例：插入两条新记录
    my_app_token = "TuSUbUniEaccHlsU387cPQgEndT"
    my_table_name = "qytang-table"

    # 注意：这里的字段名（username、password、priv、services）需和表结构中的字段名一致
    new_records = [
        {
            "username": "qytang-user14",
            "password": "Huawei@2023",
            "priv": 3,
            "services": ["ssh", "telnet"]
        },
        {
            "username": "qytang-user15",
            "password": "Cisc0123",
            "priv": 3,
            "services": ["ssh"]
        }
    ]

    insert_records_into_table(my_app_token, my_table_name, new_records)
