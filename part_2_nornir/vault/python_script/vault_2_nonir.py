from vault_1_init import client

# vault kv put qytang/cisco_ios/cred username=admin password=Cisc0123
# 获取特定secret的值
read_response = client.secrets.kv.v2.read_secret_version(
    mount_point='qytang',
    path='cisco_ios/cred',
    raise_on_deleted_version=True  # 显式设置参数为 True
)

print(read_response['data']['data'])
