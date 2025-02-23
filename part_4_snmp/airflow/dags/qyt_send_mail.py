import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from basic_info import tos, email_username, email_password, email_from


def qyt_smtp_attachment(context):
    # 使用SSL加密SMTP发送邮件, 此函数发送的邮件有主题,有正文,还可以发送附件
    date = email.utils.formatdate()  # 格式化邮件时间
    msg = MIMEMultipart()  # 产生MIME多部分的邮件信息
    # 获取任务实例
    task_instance = context.get('task_instance')
    # 获取任务状态
    task_state = task_instance.state

    # 根据任务状态设置邮件主题
    if task_state == 'success':
        subject = f"Airflow任务成功：{task_instance.task_id}"
    elif task_state == 'failed':
        subject = f"Airflow任务失败：{task_instance.task_id}"
    else:
        subject = f"Airflow任务状态：{task_instance.task_id} - {task_state}"

    msg["Subject"] = subject
    msg["From"] = email_from  # 发件人
    msg["To"] = tos  # 收件人
    msg["Date"] = date  # 发件日期

    # 邮件正文为Text类型, 使用MIMEText添加
    # MIME类型介绍 https://docs.python.org/2/library/email.mime.html
    main_body = f"""
    DAG: {context.get('task_instance').dag_id}
    任务: {context.get('task_instance').task_id}
    执行时间: {context.get('execution_date').in_timezone('Asia/Shanghai')}
    日志链接: {context.get('task_instance').log_url}
    """
    part = MIMEText(main_body)
    msg.attach(part)  # 添加正文

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 连接邮件服务器
    server.login(email_username, email_password)  # 通过用户名和密码登录邮件服务器
    failed = server.sendmail(email_from, tos, msg.as_string())  # 发送邮件
    server.quit()  # 退出会话
    if failed:
        print('Falied recipients:', failed)  # 如果出现故障，打印故障原因！
    else:
        print('邮件已经成功发出！')  # 如果没有故障发生，打印'邮件已经成功发出！'！
