from huey import RedisHuey
from redis.connection import ConnectionPool

class TaskRegistry:
    def __init__(self, redis_host='localhost', redis_port=6379):
        # Create a connection pool with retry settings
        self.pool = ConnectionPool(
            host=redis_host,
            port=redis_port,
            max_connections=20,
            retry_on_timeout=True,
            socket_keepalive=True,
            socket_timeout=300,
            retry_on_error=[TimeoutError, ConnectionError, OSError]
        )
        
        # Initialize Huey with the connection pool
        self.huey = RedisHuey(
            connection_pool=self.pool,
            connection_retries=3,
            connection_retry_delay=5
        )
        self.tasks = {}

    def register_task(self, func, **task_options):
        task = self.huey.task(**task_options)(func)
        self.tasks[func.__name__] = task
        return task

# Create registry instance
registry = TaskRegistry()

# Define your function
def my_task(param1, param2):
  # Task logic here
  return param1 + param2

# Register the task with options
my_task_registered = registry.register_task(
  my_task,
  retries=3,
  retry_delay=10,
  priority=1,
  expires=3600
)

# Usage
result = my_task_registered(1, 2)
