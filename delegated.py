from inspect import stack as _stack
# TODO: test if we can use entire module as decorator (use __init__.py)


class delegated(object):
    """Class to delegate tasks to a subordinate object.

        Subordinates can be an existing object, or the name of an instance//class attribute
        to be dynamically retrieved.

        Supervisor can be a class instance, or a dict (keys are used as attribute names).
    """

    def __init__(self, worker, attr_name=None):
        # Runs when decorating
        self.worker = worker
        self.attr_name = attr_name

    def __call__(self, func):
        # Runs when decorating, after __init__ (wraps function)
        return delegated.__proxy(self.worker, self.attr_name or func.__name__)

    class __proxy(property):
        # Builds a property object to handle proxy-ing
        def __init__(self, worker, attr_name, supervisor=None):
            if supervisor is not None:
                if isinstance(supervisor, dict):
                    def supervisor_setter(k, v):
                        return supervisor.update({k: v})
                else:
                    def supervisor_setter(k, v):
                        return setattr(supervisor, k, v)

                def deller(supervisor_instance):
                    delattr(supervisor_instance, attr_name)
            else:
                def supervisor_setter(*a, **k):
                    return None

                def deller(supervisor_instance):
                    pass

            self.attr_name = attr_name
            self.worker = worker.split('.') if isinstance(worker, str) else worker

            if isinstance(worker, str):
                self.target = '.'.join([worker, attr_name])
                getter = self.str_getter(self.worker, attr_name)
                setter = self.str_setter(self.worker, attr_name)
            else:
                self.target = '.'.join([type(worker).__qualname__, attr_name])
                getter, setter = self.obj_getter_setter(self.worker, attr_name)

            property.__init__(self, getter, setter, deller)

            supervisor_setter(attr_name, self)

        def obj_getter_setter(self, worker, attr_name):
            def getter(supervisor_instance):
                res = getattr(worker, attr_name)
                return res

            def setter(supervisor_instance, value):
                setattr(worker, attr_name, value)

            return getter, setter

        def str_getter(self, worker, attr_name):
            def getter(supervisor_instance):
                trace = [type(supervisor_instance).__name__]
                try:
                    trace.append(worker[0])
                    sub = getattr(supervisor_instance, worker[0])
                    for w in worker[1:]:
                        trace.append(w)
                        if w.endswith('()'):
                            sub = getattr(sub, w[:-2])()
                        else:
                            sub = getattr(sub, w)
                    res = getattr(sub, attr_name)
                except AttributeError:
                    raise AttributeError(f"'{'.'.join(map(str, trace))}' object has no attribute '{attr_name}'")
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
            return f"{type(self).__qualname__}({repr(self.worker)}, {repr(self.attr_name)})"

    @staticmethod
    def tasks(worker, attrs, supervisor=None):
        """Delegates attribute(s) and returns their proxies.

        :param worker: str or object; subordinate(s) to delegate to
        :param attrs: str or sequence of strings; attributes to delegate
        :param supervisor: the delegating object or `None`
        :return: a proxy (if one is requested), or list of proxies (if multiple)
        """
        proxies = []
        attrs = delegated.__split(attrs)

        if len(attrs) == 1:
            return delegated.__proxy(worker, attrs[0], supervisor)

        for attr_name in attrs:
            attr_proxy = delegated.__proxy(worker, attr_name, supervisor)
            proxies.append(attr_proxy)
        return proxies

    @staticmethod
    def here(worker, attrs):
        """Delegates attribute(s) and embeds into the containing class.

        :param worker: str or object; subordinate(s) to delegate to
        :param attrs: str or sequence of strings; attributes to delegate
        :return: a proxy (if one is requested), or list of proxies (if multiple)
        """
        supervisor = _stack()[1].frame.f_locals

        proxies = []
        attrs = delegated.__split(attrs)

        if len(attrs) == 1:
            return delegated.__proxy(worker, attrs[0], supervisor)

        for attr_name in attrs:
            attr_proxy = delegated.__proxy(worker, attr_name, supervisor)
            proxies.append(attr_proxy)
        return proxies

    @staticmethod
    def __split(attrs):
        # Split task strings by comma or space
        if isinstance(attrs, str):
            attrs = attrs.replace(',', ' ').split()
        return attrs
