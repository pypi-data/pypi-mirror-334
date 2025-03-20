def kmax(max_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg_value in args:
                if isinstance(arg_value, (int, float)) and arg_value > max_value:
                    raise ValueError(f"Value should be lesser than or equal to {max_value}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
