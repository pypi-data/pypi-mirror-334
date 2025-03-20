class Singleton:
    """
    单例基类
    """
    Instance = None

    def __new__(cls, *args, **kwargs):
        if cls.Instance is None:
            cls.Instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.Instance
