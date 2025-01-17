from huey import Huey

huey = Huey()

def my_task(arg):
    # Task logic

def wrap_with_huey_task(func):
    @huey.task()
    def wrapped_func(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped_func

# Dynamically wrap the function with the decorator
wrapped_task = wrap_with_huey_task(my_task)

# Enqueue the wrapped task
result = huey.enqueue(wrapped_task, "argument")
