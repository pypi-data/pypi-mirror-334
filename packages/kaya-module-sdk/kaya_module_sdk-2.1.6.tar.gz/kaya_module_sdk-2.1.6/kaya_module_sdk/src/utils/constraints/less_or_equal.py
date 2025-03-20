def klte(lte_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg_value in args:
                if isinstance(arg_value, (int, float)) and arg_value > lte_value:
                    raise ValueError(f"Value should be less than or equal to {lte_value}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
