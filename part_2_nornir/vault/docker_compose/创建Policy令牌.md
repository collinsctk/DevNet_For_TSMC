### policy "qytang-policy"
```shell
path "qytang/*" {
  capabilities = ["read"]
}

```

### 创建policy的Token
```shell
[root@localhost ~]# docker exec -it docker_compose-vault-1 sh
/ # export VAULT_TOKEN="hvs.5djCgwkkPtrMGnVp8HKbaiVp"
/ # vault token create -policy=qytang-policy -tls-skip-verify
Key                  Value
---                  -----
token                hvs.CAESIHIOEilXjSi4snMTRx2BzXB8fsNizJbeRP3O67VQ_3xDGh4KHGh2cy5FWmlBRG5zSlY0UDNGSFhlODVrc2pwNzI
token_accessor       5gxmBnOQAPZDydWm3TJcUZXV
token_duration       87600h
token_renewable      true
token_policies       ["default" "qytang-policy"]
identity_policies    []
policies             ["default" "qytang-policy"]

```