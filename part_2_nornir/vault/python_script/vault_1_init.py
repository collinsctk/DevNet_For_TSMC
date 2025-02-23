# pip install hvac
import hvac
import os

client = hvac.Client(
    url='https://vault.qytopensource.com:8200',
    # 使用权限被控制的令牌
    token="hvs.CAESIFvP4s6i1h1TQbIJSZu98TaOIA5l8gcHcI9V4v18eLrHGh4KHGh2cy44dEZldE5CeENpVER4aDVZdHNiRE01V0U",
    # token="hvs.6zQ8oR23bt4rJ4dV9gO98eS6",  # 管理员令牌
    verify=f"{os.path.dirname(os.path.abspath(__file__))}/ca.cer"
)

# 是否认证
print(client.is_authenticated())

# 是否解锁
print(client.sys.is_sealed())

