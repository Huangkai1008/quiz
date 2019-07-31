import os

broker_url = os.environ.get('broker_url')  # 使用RabbitMq作为消息代理
result_backend = os.environ.get('result_backend')  # 把任务结果存在Redis'
accept_content = ['json', 'msgpack', 'pickle']
task_serializer = 'json'  # 任务序列化方式
result_serializer = 'json'  # 结果序列化方式
timezone = 'Asia/Shanghai'  # 时区
enable_utc = False
# 导入任务模块
imports = ('quiz.task.email',
           'quiz.task.persist',
           )
