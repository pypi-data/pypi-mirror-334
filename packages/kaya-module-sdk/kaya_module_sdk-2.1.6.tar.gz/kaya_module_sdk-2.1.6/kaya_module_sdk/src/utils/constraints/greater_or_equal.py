def kgte(gte_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg_value in args:
                if isinstance(arg_value, (int, float)) and arg_value < gte_value:
                    raise ValueError(f"Value should be greater than or equal to {gte_value}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
