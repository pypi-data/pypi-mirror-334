import functools

def lazy_load(func):
    """Simple decorator for lazy loading attributes"""
    @functools.wraps(func)
    def wrapper(self):
        attr_name = f"_{func.__name__}"
        if not hasattr(self, attr_name) or getattr(self, attr_name) is None:
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return property(wrapper)