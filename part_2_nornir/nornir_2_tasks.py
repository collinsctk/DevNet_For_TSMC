# https://nornir.readthedocs.io/en/latest/tutorial/tasks.html
from nornir import InitNornir
# pip3 install nornir-utils
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
# Nornir加载配置文件
nr = InitNornir(config_file="config.yaml")
# 通过过滤提取,希望应用Task(任务)的主机
nr = nr.filter(
    type="router",
    # site='beijing'
)


print('-'*50 + 'hello_world' + '-'*50)


# hello world
# Task, Result都是在控制类型而已, Python函数一般不控制输入和输出类型,但是可以通过下面的方式来控制类型
# 传入的参数task类型为Task
# 输出的结果类型为Result
def hello_world(task: Task) -> Result:
    result_str = f"name:{task.host.name} site:{task.host['site']} says hello world!"
    # ~~~~ 此处可以添加各种基于host的操作 ~~~
    return Result(  # Result必须包含如下两个部分:
        host=task.host,     # 1.执行的主机
        result=result_str   # 2.执行的结果
    )


result = nr.run(
    # name='task hello world',  # 不定义name, 名字将会使用函数的名字 hello_world
    task=hello_world
)

# print_result漂亮的打印整个执行过程,打印显示而已!
print_result(result)

# 提取结果 .result与[0] 效果等价
# result['c8kv1'].result为此次任务执行的结果, result=f"{task.host.name} says hello world!"
print(f"本次任务C8Kv1的结果为: {result['c8kv1'].result}")
print(f"本次任务C8Kv2的结果为: {result['c8kv2'][0]}")

for device, task_result in result.items():
    print(f"本次任务{device.upper()}的结果为:\n"  # device就是一个字符串
          # --------------------------------------------------------
          #     return Result(  # Result必须包含如下两个部分:
          #         host=task.host,     # 1.执行的主机
          #         result=result_str   # 2.执行的结果
          #     )
          # --------------------------------------------------------
          f"\t Host:{task_result.host} \n"
          f"\t Steps:{len(task_result)} \n"
          f"\t Final Result:{task_result[0]} \n"
          f"\t Final Result:{task_result.result}")

print('-'*50 + '传参数' + '-'*50)


# 添加参数
# Task, str, Result都是在控制类型而已, 传入的参数为text, 类型为str
def say(task: Task, text: str) -> Result:
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


result = nr.run(
    name="more parameters",  # 配置了任务名称
    task=say,
    text="welcome to qytang!"  # 传递参数text
)
# print_result漂亮的打印整个执行过程,打印显示而已!
print_result(result)

# 提取结果 .result与[0] 效果等价
# result['c8kv1'].result为此次任务执行的结果, result=f"{task.host.name} says {text}"
print(f"本次任务C8Kv1的结果为: {result['c8kv1'].result}")
print(f"本次任务C8Kv2的结果为: {result['c8kv2'][0]}")


for device, task_result in result.items():
    print(f"本次任务{device.upper()}的结果为:\n"  # device就是一个字符串
          # --------------------------------------------------------
          #     return Result(
          #         host=task.host,     # 1.执行的主机
          #         result=result_str   # 2.执行的结果
          #     )
          # --------------------------------------------------------
          f"\t Host:{task_result.host} \n"
          f"\t Steps:{len(task_result)} \n"
          f"\t Final Result:{task_result[0]} \n"
          f"\t Final Result:{task_result.result}")

print('-'*50 + '一组任务' + '-'*50)


# 传入一个数, 返回一个列表字符串的函数
def count(task: Task, number: int) -> Result:
    return Result(
        host=task.host,
        result=[f'{task.host.name}:{n}' for n in range(0, number)]
    )


# 任务组
def greet_and_count(task: Task, number: int) -> Result:
    # 第一个任务say
    task1_result = task.run(
                            name="Greeting is the polite thing to do",  # 任务一
                            task=say,
                            text="hi!",
                        )

    # 第二个任务count
    task2_result = task.run(
                            name="Counting beans",  # 任务二
                            task=count,
                            number=number + int(len(task1_result.result)/10),  # 第二步可以提取第一步的运行结果
                        )

    # 第三个任务say
    task3_result = task.run(
                            name="We should say bye too",  # 任务三
                            task=say,
                            text=len(task2_result.result) * "bye!",  # 第三步可以提取第二步的运行结果
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


result = nr.run(
    name="Counting to 5 while being very polite",
    task=greet_and_count,  # 运行任务组
    number=5,  # 传入数
)

print_result(result)
# 采集C8Kv1执行的最终结果
print(f"本次任务C8Kv1的结果为: {result['c8kv1'].result}")  # result=f"{task.host} counted {even_or_odds} times!"

# 采集C8Kv2执行的最终结果
print(f"本次任务C8Kv2的结果为: {result['c8kv2'][0]}")  # result=f"{task.host} counted {even_or_odds} times!"

# -----------获取分步骤结果-----------
# 第一步结果 [第0步是最终结果]
print(f"Step1 result: {result['c8kv2'][1]}")
# 第二步结果
print(f"Step2 result: {result['c8kv2'][2]}")
# 第三步结果
print(f"Step3 result: {result['c8kv2'][3]}")

# --------------------------一次性打印所有结果--------------------------------
for device in result:
    print('-'*30 + device + '-'*30)
    print(f"本次任务{device.upper()}的最终结果为: {result[device].result}")
    for i in range(1, len(result[device])):
        print(f"本次任务{device.upper()}的{i}号任务的结果为: {result[device][i]}")