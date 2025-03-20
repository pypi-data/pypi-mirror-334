class Singleton:
    """
    单例模式基类，确保该类仅有一个实例存在。
    """
    ins = None

    def __new__(cls, *args, **kwargs):
        """
        覆盖__new__方法以控制实例创建。

        参数:
            cls: 类对象
            *args: 传递给__new__方法的位置参数
            **kwargs: 传递给__new__方法的关键字参数

        返回:
            该类的唯一实例
        """
        # 如果实例尚未创建，则创建新实例
        if cls.ins is None:
            cls.ins = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.ins
