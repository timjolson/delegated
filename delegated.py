from inspect import stack as _stack


class attr_proxy(property):
    def __init__(self, worker, attr_name, supervisor=None):
        if supervisor is not None:
            if isinstance(supervisor, str) and supervisor == '':
                supervisor = _stack()[1].frame.f_locals

            if isinstance(supervisor, dict):
                supervisorsetter = lambda k, v: supervisor.update({k: v})
            else:
                supervisorsetter = lambda k, value: setattr(supervisor, k, value)
        else:
            supervisorsetter = lambda *a: None

        def deller(master_instance):
            delattr(master_instance, attr_name)

        if isinstance(worker, str):
            self.target = '.'.join([worker, attr_name])
            getter, setter = self.str_getter_setter(worker, attr_name)

        else:
            self.target = '.'.join([type(worker).__qualname__, attr_name])
            getter, setter = self.obj_getter_setter(worker, attr_name)

        property.__init__(self, getter, setter, deller)

        self.name = attr_name
        self.worker = worker
        supervisorsetter(attr_name, self)

    def obj_getter_setter(self, worker, attr_name):
        def getter(master_instance):
            if isinstance(worker, dict): res = worker.get(attr_name)
            else: res = getattr(worker, attr_name)
            return res

        def setter(master_instance, value):
            if isinstance(worker, dict): worker.update({attr_name: value})
            else: setattr(worker, attr_name, value)
        return getter, setter

    def str_getter_setter(self, worker, attr_name):
        def getter(master_instance):
            sub = getattr(master_instance, worker)
            if isinstance(sub, dict): res = sub.get(attr_name)
            else: res = getattr(sub, attr_name)
            return res

        def setter(master_instance, value):
            sub = getattr(master_instance, worker)
            if isinstance(sub, dict): sub.update({attr_name: value})
            else: setattr(sub, attr_name, value)
        return getter, setter

    def __repr__(self):
        return f"{type(self).__qualname__}({repr(self.worker)}, {self.name})"


class method_proxy(attr_proxy):
    def obj_getter_setter(self, worker, attr_name):
        def getter(master_instance):
            if isinstance(worker, dict): res = worker.get(attr_name)
            else: res = getattr(worker, attr_name)
            return res

        def setter(master_instance, value):
            setattr(master_instance, attr_name, value)

        return getter, setter

    def str_getter_setter(self, worker, attr_name):
        def getter(master_instance):
            sub = getattr(master_instance, worker)
            if isinstance(sub, dict): res = sub.get(attr_name)
            else: res = getattr(sub, attr_name)
            return res

        def setter(master_instance, value):
            setattr(master_instance, attr_name, value)

        return getter, setter


class delegated():
    def __init__(self, worker, attr_name=None):
        self.worker = worker
        self.attr_name = attr_name

    def __call__(self, func):
        return delegated.method(self.worker, self.attr_name or func.__name__)

    class attribute(attr_proxy):
        pass

    @staticmethod
    def attributes(worker, attrs, supervisor=None):
        if isinstance(supervisor, str) and supervisor == '':
            supervisor = _stack()[1].frame.f_locals

        proxies = []
        for attr_name in delegated.split(attrs):
            attr_proxy = delegated.attribute(worker, attr_name, supervisor)
            proxies.append(attr_proxy)
        return proxies

    class method(method_proxy):
        pass

    @staticmethod
    def methods(worker, attrs, supervisor=None):
        if isinstance(supervisor, str) and supervisor == '':
            supervisor = _stack()[1].frame.f_locals

        proxies = []
        for attr_name in delegated.split(attrs):
            method_proxy = delegated.method(worker, attr_name, supervisor)
            proxies.append(method_proxy)
        return proxies

    @staticmethod
    def split(attrs):
        if isinstance(attrs, str):
            attrs = attrs.replace(',', ' ').split()
        return attrs
