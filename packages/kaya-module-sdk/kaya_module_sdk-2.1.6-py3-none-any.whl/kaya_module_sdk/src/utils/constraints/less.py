def klt(lt_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg_value in args:
                if isinstance(arg_value, (int, float)) and arg_value >= lt_value:
                    raise ValueError(f"Value should be less than {lt_value}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
