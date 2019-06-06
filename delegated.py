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

        def deller(supervisor_instance):
            delattr(supervisor_instance, attr_name)

        self.name = attr_name
        self.worker = worker.split('.') if isinstance(worker, str) else worker

        if isinstance(worker, str):
            self.target = '.'.join([worker, attr_name])
            getter = self.str_getter(self.worker, attr_name)
            setter = self.str_setter(self.worker, attr_name)
        else:
            self.target = '.'.join([type(worker).__qualname__, attr_name])
            getter, setter = self.obj_getter_setter(self.worker, attr_name)

        property.__init__(self, getter, setter, deller)

        supervisorsetter(attr_name, self)

    def obj_getter_setter(self, worker, attr_name):
        def getter(supervisor_instance):
            res = getattr(worker, attr_name)
            return res

        def setter(supervisor_instance, value):
            setattr(worker, attr_name, value)
        return getter, setter

    def str_getter(self, worker, attr_name):
        def getter(supervisor_instance):
            sub = getattr(supervisor_instance, worker[0])
            for w in worker[1:]:
                if w.endswith('()'):
                    sub = getattr(sub, w[:-2])()
                else:
                    sub = getattr(sub, w)
            res = getattr(sub, attr_name)
            return res
        return getter

    def str_setter(self, worker, attr_name):
        def setter(supervisor_instance, value):
            sub = getattr(supervisor_instance, worker[0])
            for w in worker[1:]:
                if w.endswith('()'):
                    sub = getattr(sub, w[:-2])()
                else:
                    sub = getattr(sub, w)
            setattr(sub, attr_name, value)
        return setter

    def __repr__(self):
        return f"{type(self).__qualname__}({repr(self.worker)}, {self.name})"


class method_proxy(attr_proxy):
    def str_setter(self, worker, attr_name):
        def setter(supervisor_instance, value):
            setattr(supervisor_instance, attr_name, value)
        return setter


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
