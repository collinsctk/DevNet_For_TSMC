# pip3.11 install lark-oapi
import json
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import CreateAppTableRequest, CreateAppTableResponse
from lark_oapi.api.bitable.v1.model import (
    CreateAppTableRequestBody,
    ReqTable,
    AppTableCreateHeader,
    AppTableFieldProperty,
    AppTableFieldPropertyOption
)
from huawei_1_netmiko.feishu_sdk.basic_info import app_id, app_secret, my_app_token


def create_table(app_token: str, table_name: str):
    # 1. 创建client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 2. 构造请求对象 - 指定要在哪个 Base (app_token) 下创建数据表
    #    以及表格的默认视图名称、各个字段配置
    request = CreateAppTableRequest.builder() \
        .app_token(app_token) \
        .request_body(
            CreateAppTableRequestBody.builder()
            .table(
                ReqTable.builder()
                .name(table_name)               # 新数据表的名称
                .default_view_name("default")     # 可以自定义这个视图名
                .fields([
                    # 1) username - 文本类型（type=1）
                    AppTableCreateHeader.builder()
                    .field_name("username")
                    .type(1)  # 1: 文本
                    .build(),

                    # 2) password - 文本类型（type=1）
                    AppTableCreateHeader.builder()
                    .field_name("password")
                    .type(1)  # 1: 文本
                    .build(),

                    # 3) priv - 数字类型（type=2）
                    AppTableCreateHeader.builder()
                    .field_name("priv")
                    .type(2)  # 2: 数字
                    .build(),

                    # 4) services - 多选类型（type=4）
                    AppTableCreateHeader.builder()
                    .field_name("services")
                    .type(4)  # 4: 多选
                    # 为多选字段配置一些可选项（可以在此定义选项名、颜色等）
                    .property(
                        AppTableFieldProperty.builder()
                        .options([
                            AppTableFieldPropertyOption.builder().name("ssh").color(0).build(),
                            AppTableFieldPropertyOption.builder().name("telnet").color(1).build(),
                            AppTableFieldPropertyOption.builder().name("http").color(2).build()
                        ])
                        .build()
                    )
                    .build()
                ])
                .build()
            )
            .build()
        ) \
        .build()

    # 3. 发起请求
    response: CreateAppTableResponse = client.bitable.v1.app_table.create(request)

    # 4. 处理失败返回
    if not response.success():
        print(
            f"创建数据表失败，code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: "
            f"\n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}"
        )
        return

    # 5. 创建成功 - 输出结果
    return {"table_id": response.data.table_id,
            "default_view_id": response.data.default_view_id}


if __name__ == "__main__":
    from feishu_3_insert_data import insert_records_into_table
    from datetime import datetime
    table_name = f"test_table_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    # my_app_token = "TuSUbUniEaccHlsU387cPQgEndT" ~~~~多维表格的ID
    create_table(my_app_token, table_name)
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

    insert_records_into_table(my_app_token, table_name, new_records)
