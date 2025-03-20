import inspect


def kmaxlen(max_len_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # NOTE: Use inspect to check if the function is a method
            signature = inspect.signature(func)
            # NOTE: If the method has 'self' or 'cls' as its first parameter, it's a method
            parameters = list(signature.parameters.keys())
            if len(parameters) > 0 and parameters[0] in ["self", "cls"]:
                # NOTE: If it's a method, exclude `self` or `cls` from the argument length check
                sanitized_args = args[1:]
            else:
                # NOTE: Otherwise, treat it as a normal function
                sanitized_args = args
            if len(sanitized_args) > max_len_value:
                raise ValueError(f"Composite type length should not be above {max_len_value}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
