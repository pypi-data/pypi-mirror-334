# celeryconfig.py
import os

pleach_redis_host = os.environ.get("PLEACH_REDIS_HOST")
pleach_redis_port = os.environ.get("PLEACH_REDIS_PORT")
# broker default user

if pleach_redis_host and pleach_redis_port:
    broker_url = f"redis://{pleach_redis_host}:{pleach_redis_port}/0"
    result_backend = f"redis://{pleach_redis_host}:{pleach_redis_port}/0"
else:
    # RabbitMQ
    mq_user = os.environ.get("RABBITMQ_DEFAULT_USER", "pleach")
    mq_password = os.environ.get("RABBITMQ_DEFAULT_PASS", "pleach")
    broker_url = os.environ.get("BROKER_URL", f"amqp://{mq_user}:{mq_password}@localhost:5672//")
    result_backend = os.environ.get("RESULT_BACKEND", "redis://localhost:6379/0")
# tasks should be json or pickle
accept_content = ["json", "pickle"]
