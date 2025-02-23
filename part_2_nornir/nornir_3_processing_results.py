# https://nornir.readthedocs.io/en/latest/tutorial/task_results.html
import logging
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result

# Nornir加载配置文件
nr = InitNornir(config_file="config.yaml")

# 通过过滤提取,希望应用Task(任务)的设备, 类型为router的设备
cmh = nr.filter(type="router")


# 传入一个数, 返回一个列表字符串的函数
def count(task: Task, number: int) -> Result:
    return Result(
        host=task.host,
        result=[f'{task.host.name}:{n}' for n in range(0, number)]
    )


# 修改原始的say函数, 在特定条件下抛出异常
def say(task: Task, text: str) -> Result:
    # 条件语句实战， 如果是C8Kv1强行抛出异常
    if task.host.name == "c8kv1":
        raise Exception("I can't say anything right now")
        # -------------------------------------强行抛出告警--------------------------------------
        # vvvv Counting to 5 while being very polite ** changed : False vvvvvvvvvvvvvvvvvv ERROR
        # Subtask: Greeting is the polite thing to do (failed)
        #
        # ---- Greeting is the polite thing to do ** changed : False --------------------- ERROR
        # Traceback (most recent call last):
        #   File "/root/.virtualenvs/opensourcesoftware/lib/python3.11/site-packages/nornir/core/task.py", line 98,
        #   in start
        #     r = self.task(self, **self.params)
        #         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #   File "/opensourcesoftware/open_source_software_1_2_Nornir/nornir_3_processing_results.py", line 26, in say
        #     raise Exception("I can't say anything right now")
        # Exception: I can't say anything right now

    # 可以把任务中每一个host的属性提取出来
    # task.host.name
    # task.host.hostname
    # 提取host的数据(data)下的键'site'所对应的值
    # task.host['site']
    result_str = f"{task.host.name} ({task.host.hostname}) says {text} at site {task.host['site']}"  # 做了一个简单的字符串拼接
    # ~~~~ 此处可以添加各种基于host的操作 ~~~
    return Result(
        host=task.host,     # 1.执行的主机
        result=result_str   # 2.执行的结果
    )


# 任务组
def greet_and_count(task: Task, number: int):
    # 第一个任务say
    task1_result = task.run(
                            name="Greeting is the polite thing to do",  # 任务一
                            severity_level=logging.DEBUG,  # 设置任务的日志级别, 默认级别为INFO
                            task=say,
                            text="hi!",
                        )

    # 第二个任务count
    task2_result = task.run(
                            name="Counting beans",  # 任务二
                            task=count,
                            number=number + int(len(task1_result.result)/10),  # 第二步可以提起第一步的运行结果
                        )

    # 第三个任务say
    task3_result = task.run(
                            name="We should say bye too",  # 任务三
                            severity_level=logging.DEBUG,  # 设置任务的日志级别, 默认级别为INFO
                            task=say,
                            text=len(task2_result.result) * "bye!",  # 第三步可以提起第二步的运行结果
                        )

    # 可以采集之前任务执行的结果， 然后进行操作
    # ~~~ 此处可以添加更多逻辑操作 ~~~
    final_number = len(task1_result.result) + len(task2_result.result) + len(task3_result.result) + number

    # 判断最终的数final_number是奇数还是偶数
    even_or_odds = "odd" if final_number % 2 == 1 else "even"  # 条件语句
    return Result(
        host=task.host,  # 应用到主机
        result=f"{task.host} counted {even_or_odds} times!",  # 返回最终结果
    )


result = cmh.run(
    name="Counting to 5 while being very polite",
    task=greet_and_count,  # 运行任务组
    number=5,  # 传入数
)

# 默认print_result打印级别为INFO以上事件, 设置成为logging.DEBUG的任务将不会被打印显示
print('-'*50 + 'print_result执行结果' + '-'*50)
print_result(result)
print('-'*50 + 'print_result执行结果' + '-'*50)

# -------------------------------------------------C8Kv1执行结果（抛出异常就结束了）-------------------------------------------------
# Counting to 5 while being very polite*******************************************
# * c8kv1 ** changed : False *****************************************************
# vvvv Counting to 5 while being very polite ** changed : False vvvvvvvvvvvvvvvvvv ERROR
# Subtask: Greeting is the polite thing to do (failed)
#
# ---- Greeting is the polite thing to do ** changed : False --------------------- ERROR
# Traceback (most recent call last):
#   File "/root/.virtualenvs/opensourcesoftware/lib/python3.11/site-packages/nornir/core/task.py", line 98, in start
#     r = self.task(self, **self.params)
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/opensourcesoftware/open_source_software_1_2_Nornir/nornir_3_processing_results.py", line 26, in say
#     raise Exception("I can't say anything right now")
# Exception: I can't say anything right now

# -------------------------------------------------C8Kv2执行结果（只打印了最终结果，和第二步任务！）-------------------------------------------------
# * c8kv2 ** changed : False *****************************************************
# vvvv Counting to 5 while being very polite ** changed : False vvvvvvvvvvvvvvvvvv INFO
# c8kv2 counted odd times!
# ---- Counting beans ** changed : False ----------------------------------------- INFO
# [ 'c8kv2:0',
#   'c8kv2:1',
#   'c8kv2:2',
#   'c8kv2:3',
#   'c8kv2:4',
#   'c8kv2:5',
#   'c8kv2:6',
#   'c8kv2:7',
#   'c8kv2:8']
# ^^^^ END Counting to 5 while being very polite ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ========================官方对打印严重级别的介绍========================
# As you probably noticed, not all the tasks were printed.
# This is due to the severity_level argument we passed.
# This let’s us flag tasks with any of the logging levels.
# Then print_result is able to follow logging rules to print the results.
# By default only tasks marked as INFO will be printed
# (this is also the default for the tasks if none is specified).

# 可以修改print_result打印的级别为logging.DEBUG, 这样就可以打印所有的事件!
print('-'*50 + 'print_result 打印的级别为logging.DEBUG 执行结果' + '-'*50)
print_result(result, severity_level=logging.DEBUG)
print('-'*50 + 'print_result 打印的级别为logging.DEBUG 执行结果' + '-'*50)

# 选择打印某一个步骤
print('-'*50 + 'print_result 打印某一个步骤 执行结果' + '-'*50)
print_result(result['c8kv2'][2])
print('-'*50 + 'print_result 打印某一个步骤 执行结果' + '-'*50)
# 你可以提取什么设备'c8kv1',第几次任务的结果
# .result 为 最终返回结果              :c8kv1 counted odd times!
# [0] 为 最终返回结果                  :c8kv1 counted odd times!
# [1] 为 第一个task say的返回结果       :c8kv1 says hi!
# [2] 为 task count的返回结果          :[0, 1, 2, 3, 4]
# [3] 为 第二个task say的返回结果       :c8kv1 says bye!
print(result['c8kv2'].result)
print(result['c8kv2'][0])
print(result['c8kv2'][1])
print(result['c8kv2'][2])
print(result['c8kv2'][3])

# 查看任何一个设备的任务是否failed
print('-'*50 + '查看任何一个设备的任务是否failed' + '-'*50)
print("if failed: ", result["c8kv1"].failed)

# 最终任务changed的结果
print('-'*50 + '最终任务changed的结果' + '-'*50)
print("changed: ", result["c8kv2"].changed)

# 每一个小步骤changed的结果
print('-'*50 + '每一个小步骤changed的结果' + '-'*50)
print("changed: ", result["c8kv2"][1].changed)
