
def singleton(cls):
    """
    Singleton decorator to ensure that a class has only one instance 
    and provide a global point of access to it. 
    
    See:
       * Design patterns: <a href="https://refactoring.guru/design-patterns/singleton">Singleton - refactoring.guru</a>
    
    Usage:
    ```python
        @singleton
        class MyClass:
            pass

        instance1 = MyClass()
        instance2 = MyClass()

        assert instance1 is instance2  # True, both variables point to the same instance.
    ```
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
