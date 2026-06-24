from functools import wraps


def display_module(func):
    """
    Не особо пригодился этот декоратор, решил перейти глобально на rich.Panels, но пока что оставлю
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0]
        print(str(f"| {instance.module} |").center(32, "-"))
        # instance.output.display_panel(text, str(instance.module))
        return func(*args, **kwargs)

    return wrapper
