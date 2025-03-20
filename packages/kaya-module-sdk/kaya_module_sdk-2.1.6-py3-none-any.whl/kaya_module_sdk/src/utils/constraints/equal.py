def keq(eq_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg_value in args:
                if isinstance(arg_value, (int, float)) and arg_value != eq_value:
                    raise ValueError(f"Value should be equal to {eq_value}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
