### 测试代码
```shell
[root@QYTRocky ~]# /usr/bin/python3.11 /NetDevOps_Huawei/huawei_3_snmp/practice_lab/orm_2_write_db.py
```

### crond调度
```shell
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed
# * * * * * root /usr/bin/python3.11 /NetDevOps_Huawei_Homework/day_4_backup_config_crond/day_4_2_backup_config.py
* * * * * root /usr/bin/python3.11 /NetDevOps_Huawei/huawei_3_snmp/practice_lab/orm_2_write_db.py

```

### 重启服务
```shell
[root@QYTRocky ~]# systemctl restart crond.service

```
