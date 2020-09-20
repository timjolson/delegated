from inspect import stack as _stack
import types
import sys
import logging
logger = logging.getLogger(__name__)


class delegated(object):
    logger = logger
    """Class to delegate tasks to a subordinate object.
    Create proxies to methods or attributes via decorator, assignment, or automatic class embedding.

    Subordinates can be an existing object, or the name of an instance//class attribute
    to be dynamically retrieved.
    """
    @staticmethod
    def tasks(worker, attrs, supervisor=None):
        """Delegates attribute(s) and returns their proxies.

        :param worker: str or object; subordinate(s) to delegate to
        :param attrs: str or sequence of strings; attributes to delegate
        :param supervisor: the delegating object or `None`
        :return: a proxy (if one is requested), or list of proxies (if multiple requested)
        """
        logger.debug(str(dict(worker=worker, attrs=attrs, supervisor=supervisor)))
        proxies = []
        attrs = delegated.__split(attrs)

        if len(attrs) == 1:
            logger.debug('return')
            return delegated.__proxy(worker, attrs[0], supervisor)

        for attr_name in attrs:
            attr_proxy = delegated.__proxy(worker, attr_name, supervisor)
            proxies.append(attr_proxy)
        logger.debug('return')
        return proxies

    @staticmethod
    def here(worker, attrs):
        """Delegates attribute(s) and embeds into the containing class.

        :param worker: str or object; subordinate(s) to delegate to
        :param attrs: str or sequence of strings; attributes to delegate
        :return: a proxy (if one is requested), or list of proxies (if multiple requested)
        """
        supervisor = _stack()[1].frame.f_locals
        logger.debug(str(dict(worker=worker, attrs=attrs, supervisor=supervisor)))
        return delegated.tasks(worker, attrs, supervisor=supervisor)

    def __init__(self, worker, attr_name=None):
        # Runs when decorating
        logger.debug(str(dict(worker=worker, attr_name=attr_name)))
        self.worker = worker
        self.attr_name = attr_name

    def __call__(self, func):
        # Runs when decorating, after __init__ (wraps function)
        logger.debug(str(func))
        return delegated.__proxy(self.worker, self.attr_name or func.__name__)

    class __proxy(property):
        # Builds a property object to handle proxy-ing
        def __init__(self, worker, attr_name, supervisor=None):
            logger.debug(str(dict(worker=worker, attr_name=attr_name, supervisor=supervisor)))
            if supervisor is not None:
                logger.debug('making dict setter')
                def supervisor_setter(k, v):
                    logger.debug('run dict setter')
                    return supervisor.update({k: v})
            else:
                def supervisor_setter(*a, **k):
                    return None

            self.attr_name = attr_name
            self.worker = worker.split('.') if isinstance(worker, str) else worker

            if isinstance(worker, str):
                logger.debug('isinstance worker/str')
                self.target = '.'.join([worker, attr_name])
                getter = self.str_getter(self.worker, attr_name)
                setter = self.str_setter(self.worker, attr_name)
            else:
                logger.debug('worker is object')
                self.target = '.'.join([type(worker).__qualname__, attr_name])
                getter, setter = self.obj_getter_setter(self.worker, attr_name)

            property.__init__(self, getter, setter)

            supervisor_setter(attr_name, self)

        def obj_getter_setter(self, worker, attr_name):
            logger.debug(str(dict(worker=worker, attr_name=attr_name)))
            def getter(supervisor_instance):
                logger.debug(str(dict(worker=worker, attr_name=attr_name)))
                res = getattr(worker, attr_name)
                return res

            def setter(supervisor_instance, value):
                logger.debug(str(dict(value=value)))
                setattr(worker, attr_name, value)

            return getter, setter

        def str_getter(self, worker, attr_name):
            logger.debug(str(dict(worker=worker, attr_name=attr_name)))
            def getter(supervisor_instance):
                logger.debug('')
                trace = [type(supervisor_instance).__name__, worker[0]]
                remaining = worker.copy() + [attr_name]
                try:
                    sub = getattr(supervisor_instance, worker[0])
                    logger.debug('')
                    del remaining[0]
                    for w in worker[1:]:
                        logger.debug(str(dict(worker=worker)))
                        if w.endswith('()'):
                            sub = getattr(sub, w[:-2])()
                        else:
                            sub = getattr(sub, w)
                        trace.append(w)
                        logger.debug(str(dict(trace=trace)))
                        del remaining[0]
                    logger.debug(str(dict(sub=sub, attr_name=attr_name)))
                    res = getattr(sub, attr_name)
                except AttributeError as err:
                    msg = f"By delegated proxy: '{'.'.join(map(str, trace))}' " \
                          f"object has no attribute '{remaining[0]}'"
                    delegated._shallow_exception(err, message=msg, off_the_top=2)

                return res

            return getter

        def str_setter(self, worker, attr_name):
            logger.debug(str(dict(worker=worker, attr_name=attr_name)))
            def setter(supervisor_instance, value):
                logger.debug(str(dict(value=value)))
                sub = getattr(supervisor_instance, worker[0])
                for w in worker[1:]:
                    if w.endswith('()'):
                        sub = getattr(sub, w[:-2])()
                        logger.debug(str(dict(sub=sub)))
                    else:
                        sub = getattr(sub, w)
                        logger.debug(str(dict(sub=sub)))
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

    @staticmethod
    def _shallow_exception(exception, message=None, off_the_top=0):
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
