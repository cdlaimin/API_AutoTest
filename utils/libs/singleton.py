import threading
import weakref


class Singleton(type):
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Singleton.__instance = None

        # 创建一个弱引用类型的字典，其值必须是一个对象。当对应的key没有被强引用时，系统将回收其键值对内存
        self._cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        kargs = ''.join('%s' % key for key in args) if args else ''
        kkwargs = ''.join(list('%s' % key for key in kwargs.keys())) if kwargs else ''
        if kargs + kkwargs not in self._cache:
            with Singleton._instance_lock:
                Singleton.__instance = super().__call__(*args, **kwargs)
                self._cache[kargs + kkwargs] = Singleton.__instance
        else:
            Singleton.__instance = self._cache[kargs + kkwargs]
        return Singleton.__instance
