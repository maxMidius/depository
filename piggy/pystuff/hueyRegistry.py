from huey import RedisHuey

class TaskRegistry:
  def __init__(self):
      self.huey = RedisHuey()
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
