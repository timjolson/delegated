from inspect import stack as _stack
import types
import sys
# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


def __shallow_exception(exception, message=None, off_the_top=0):
    exp = type(exception)
    tb = None
    while True:
        try:
            frame = sys._getframe(off_the_top)
            off_the_top += 1
        except ValueError as exc:
            break

        tb = types.TracebackType(tb, frame, frame.f_lasti, frame.f_lineno)

        raise exp(message if message is not None else exception.args).with_traceback(tb)


class delegated(object):
    # logger = logger
    """Class to delegate tasks to a subordinate object.
    Create proxies to methods or attributes via decorator, assignment, or automatic class embedding.

    Subordinates can be an existing object, or the name of an instance//class attribute
    to be dynamically retrieved.

    Supervisor can be a class instance, or a dict (keys are used as attribute names).
    """
    @staticmethod
    def tasks(worker, attrs, supervisor=None):
        """Delegates attribute(s) and returns their proxies.

        :param worker: str or object; subordinate(s) to delegate to
        :param attrs: str or sequence of strings; attributes to delegate
        :param supervisor: the delegating object or `None`
        :return: a proxy (if one is requested), or list of proxies (if multiple requested)
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
        :return: a proxy (if one is requested), or list of proxies (if multiple requested)
        """
        supervisor = _stack()[1].frame.f_locals
        return delegated.tasks(worker, attrs, supervisor=supervisor)

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
                trace = [type(supervisor_instance).__name__, worker[0]]
                remaining = worker.copy() + [attr_name]
                try:
                    sub = getattr(supervisor_instance, worker[0])
                    del remaining[0]
                    for w in worker[1:]:
                        if w.endswith('()'):
                            sub = getattr(sub, w[:-2])()
                        else:
                            sub = getattr(sub, w)
                        trace.append(w)
                        del remaining[0]
                    res = getattr(sub, attr_name)
                except AttributeError as err:
                    msg = f"By `delegated` proxy: '{'.'.join(map(str, trace))}' " \
                          f"object has no attribute '{remaining[0]}'"
                    delegated.__shallow_exception(err, message=msg, off_the_top=2)

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
    def __split(attrs):
        # Split task strings by comma or space
        if isinstance(attrs, str):
            attrs = attrs.replace(',', ' ').split()
        return attrs
