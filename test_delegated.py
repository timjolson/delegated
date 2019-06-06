import pytest
from .delegated import attr_proxy, method_proxy, delegated


class Subordinate():
    def method1(self, *args, **kwargs):
        return 'method1', self, args, kwargs
    def method2(self, *args, **kwargs):
        return 'method2', self, args, kwargs
    def method3(self, *args, **kwargs):
        return 'method3', self, args, kwargs
    attr1 = 'sub attr1'
    attr2 = 'sub attr2'
    attr3 = 'sub attr3'


def check_method1(m):
    assert m.method1() == ("method1", m.sub, (), {}), '0 {0} != {1}'.format(m.method1(), ("method1", m.sub, (), {}))
    assert m.method1() == m.sub.method1()
    args = ('a', 'b')
    kwargs = {'c': 'C', 'd': 'D'}
    assert m.method1(*args, **kwargs) == ("method1", m.sub, args, kwargs)
    assert m.method1(*args, **kwargs) == m.sub.method1(*args, **kwargs)


def check_method2(m):
    assert m.method2() == ("method2", m.sub, (), {}), '1 {0} != {1}'.format(m.method2(), ("method2", m.sub, (), {}))
    assert m.method2() == m.sub.method2()
    args = ('a', 'b')
    kwargs = {'c': 'C', 'd': 'D'}
    assert m.method2(*args, **kwargs) == ("method2", m.sub, args, kwargs)
    assert m.method2(*args, **kwargs) == m.sub.method2(*args, **kwargs)


def check_method3(m):
    assert m.method3() == ("method1", m.sub, (), {}), '2 {0} != {1}'.format(m.method3(), ("method1", m.sub, (), {}))
    assert m.method3() == m.sub.method1()
    args = ('a', 'b')
    kwargs = {'c': 'C', 'd': 'D'}
    assert m.method3(*args, **kwargs) == ("method1", m.sub, args, kwargs)
    assert m.method3(*args, **kwargs) == m.sub.method1(*args, **kwargs)


def check_methods(m):
    check_method1(m)
    check_method2(m)
    check_method3(m)


def check_attr1(m):
    assert m.attr1 == 'sub attr1'
    m.attr1 = 'test'
    assert m.attr1 == 'test'
    assert m.attr1 == m.sub.attr1, '{0} != {1}'.format(m.attr1, m.sub.attr1)
    m.attr1 = 'sub attr1'


def check_attr2(m):
    assert m.attr2 == 'sub attr2'
    m.attr2 = 'test'
    assert m.attr2 == 'test'
    assert m.attr2 == m.sub.attr2, '{0} != {1}'.format(m.attr2, m.sub.attr2)
    m.attr2 = 'sub attr2'


def check_attr3(m):
    assert m.attr3 == 'sub attr1'
    m.attr3 = 'test'
    assert m.attr3 == 'test'
    assert m.attr3 == m.sub.attr1, '{0} != {1}'.format(m.attr3, m.sub.attr1)
    m.attr3 = 'sub attr1'


def check_attrs(m):
    check_attr1(m)
    check_attr2(m)
    check_attr3(m)


def test_attr_proxy_class():
    class Master():
        sub = Subordinate()
        attr1 = attr_proxy('sub', 'attr1')
        attr2 = attr_proxy('sub', 'attr2')
        attr3 = attr_proxy('sub', 'attr1')

    check_attrs(Master())

    class Master():
        sub = Subordinate()
        attr1 = attr_proxy(sub, 'attr1')
        attr2 = attr_proxy(sub, 'attr2')
        attr3 = attr_proxy(sub, 'attr1')

    check_attrs(Master())


def test_attr_proxy_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        attr1 = attr_proxy('sub', 'attr1')
        attr2 = attr_proxy('sub', 'attr2')
        attr3 = attr_proxy('sub', 'attr1')

    check_attrs(Master())


def test_method_proxy_class():
    class Master():
        sub = Subordinate()
        method1 = method_proxy('sub', 'method1')
        method2 = method_proxy('sub', 'method2')
        method3 = method_proxy('sub', 'method1')

    check_methods(Master())

    class Master():
        sub = Subordinate()
        method1 = method_proxy(sub, 'method1')
        method2 = method_proxy(sub, 'method2')
        method3 = method_proxy(sub, 'method1')

    check_methods(Master())


def test_method_proxy_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        method1 = method_proxy('sub', 'method1')
        method2 = method_proxy('sub', 'method2')
        method3 = method_proxy('sub', 'method1')

    check_methods(Master())


def test_decorator_class():
    class Master():
        sub = Subordinate()

        @delegated('sub')
        def method1(self, *args, **kwargs): pass
        @delegated('sub')
        def method2(self, *args, **kwargs): pass
        @delegated('sub', 'method1')
        def method3(self, *args, **kwargs): pass

    check_methods(Master())

    class Master():
        sub = Subordinate()

        @delegated(sub)
        def method1(self, *args, **kwargs): pass
        @delegated(sub)
        def method2(self, *args, **kwargs): pass
        @delegated(sub, 'method1')
        def method3(self, *args, **kwargs): pass

    check_methods(Master())


def test_decorator_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()

        @delegated('sub')
        def method1(self, *args, **kwargs): pass
        @delegated('sub')
        def method2(self, *args, **kwargs): pass
        @delegated('sub', 'method1')
        def method3(self, *args, **kwargs): pass

    check_methods(Master())


def test_method_class():
    class Master():
        sub = Subordinate()
        method1 = delegated.method('sub', 'method1')
        method2 = delegated.method('sub', 'method2')
        method3 = delegated.method('sub', 'method1')

    check_methods(Master())

    class Master():
        sub = Subordinate()
        method1 = delegated.method(sub, 'method1')
        method2 = delegated.method(sub, 'method2')
        method3 = delegated.method(sub, 'method1')

    check_methods(Master())


def test_method_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        method1 = delegated.method('sub', 'method1')
        method2 = delegated.method('sub', 'method2')
        method3 = delegated.method('sub', 'method1')

    check_methods(Master())


def test_attr_class():
    class Master():
        sub = Subordinate()
        attr1 = delegated.attribute('sub', 'attr1')
        attr2 = delegated.attribute('sub', 'attr2')
        attr3 = delegated.attribute('sub', 'attr1')

    check_attrs(Master())

    class Master():
        sub = Subordinate()
        attr1 = delegated.attribute(sub, 'attr1')
        attr2 = delegated.attribute(sub, 'attr2')
        attr3 = delegated.attribute(sub, 'attr1')

    check_attrs(Master())


def test_attr_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        attr1 = delegated.attribute('sub', 'attr1')
        attr2 = delegated.attribute('sub', 'attr2')
        attr3 = delegated.attribute('sub', 'attr1')

    check_attrs(Master())


def test_basics_multiple_instances():
    class Master():
        def __init__(self):
            self.sub = Subordinate()

        attr1 = delegated.attribute('sub', 'attr1')
        attr2 = delegated.attribute('sub', 'attr2')
        attr3 = delegated.attribute('sub', 'attr1')

        shared = Subordinate()
        shared_attr = delegated.attribute('shared', 'attr1')

    m1, m2 = Master(), Master()

    check_attrs(m1)
    check_attrs(m2)

    assert m1.attr1 == m2.attr1
    m1.attr1 = 'changed m1'
    assert m1.attr1 != m2.attr1
    assert m1.attr1 == m1.attr3

    assert m2.attr1 == m2.attr3
    m2.attr3 = 'changed m2'
    assert m2.attr1 == m2.attr3
    assert m1.attr1 != m2.attr1

    assert m1.shared_attr == m2.shared_attr
    m1.shared_attr = 'changed shared m1'
    assert m2.shared_attr == 'changed shared m1'
    assert m1.shared_attr == m2.shared_attr


def test_methods_class():
    class Master():
        sub = Subordinate()
        method1, method2 = delegated.methods('sub', 'method1 method2')
        method3 = delegated.method('sub', 'method1')

    check_methods(Master())

    class Master():
        sub = Subordinate()
        method1, method2 = delegated.methods(sub, ['method1', 'method2'])
        method3 = delegated.method(sub, 'method1')

    check_methods(Master())


def test_methods_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        method1, method2 = delegated.methods('sub', 'method1 method2')
        method3 = delegated.method('sub', 'method1')

    check_methods(Master())


def test_attrs_class():
    class Master():
        sub = Subordinate()
        attr1, attr2 = delegated.attributes('sub', 'attr1 attr2')
        attr3 = delegated.attribute('sub', 'attr1')

    check_attrs(Master())

    class Master():
        sub = Subordinate()
        attr1, attr2 = delegated.attributes(sub, 'attr1 attr2')
        attr3 = delegated.attribute(sub, 'attr1')

    check_attrs(Master())


def test_attrs_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        attr1, attr2 = delegated.attributes('sub', 'attr1 attr2')
        attr3 = delegated.attribute('sub', 'attr1')

    check_attrs(Master())


def test_method_here_class():
    class Master():
        sub = Subordinate()
        delegated.method('sub', 'method1', '')
        delegated.method('sub', 'method2', '')

    check_method1(Master())
    check_method2(Master())

    class Master():
        sub = Subordinate()
        delegated.method(sub, 'method1', '')
        delegated.method(sub, 'method2', '')

    check_method1(Master())
    check_method2(Master())


def test_method_here_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()

        delegated.method('sub', 'method1', '')
        delegated.method('sub', 'method2', '')

    check_method1(Master())
    check_method2(Master())


def test_methods_here_class():
    class Master():
        sub = Subordinate()
        delegated.methods('sub', 'method1, method2', '')

    check_method1(Master())
    check_method2(Master())

    class Master():
        sub = Subordinate()
        delegated.methods(sub, 'method1, method2', '')

    check_method1(Master())
    check_method2(Master())


def test_methods_here_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        delegated.methods('sub', 'method1, method2', '')

    check_method1(Master())
    check_method2(Master())


def test_attr_here_class():
    class Master():
        sub = Subordinate()
        delegated.attribute('sub', 'attr1', '')
        delegated.attribute('sub', 'attr2', '')

    check_attr1(Master())
    check_attr2(Master())

    class Master():
        sub = Subordinate()
        delegated.attribute(sub, 'attr1', '')
        delegated.attribute(sub, 'attr2', '')

    check_attr1(Master())
    check_attr2(Master())


def test_attr_here_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        delegated.attribute('sub', 'attr1', '')
        delegated.attribute('sub', 'attr2', '')

    check_attr1(Master())
    check_attr2(Master())


def test_attrs_here_class():
    class Master():
        sub = Subordinate()
        delegated.attributes('sub', 'attr1, attr2', '')

    check_attr1(Master())
    check_attr2(Master())

    class Master():
        sub = Subordinate()
        delegated.attributes(sub, 'attr1, attr2', '')

    check_attr1(Master())
    check_attr2(Master())


def test_attrs_here_instance():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        delegated.attributes('sub', 'attr1, attr2', '')

    check_attr1(Master())
    check_attr2(Master())


def test_nested_attr():
    class nested_call_helper(Subordinate):
        call_sub = Subordinate()
        call_sub.attr1 = 'call sub attr1'
        def call_test(self):
            return self.call_sub

    class deep_nested_helper(Subordinate):
        deep_call_sub = nested_call_helper()
        def call_test(self):
            return self.deep_call_sub

    class Master():
        def __init__(self):
            self.sub = Subordinate()
            self.sub.sub2 = nested_call_helper()
            self.sub.sub2.sub3 = deep_nested_helper()
            self.sub.sub2.sub3.sub4 = Subordinate()
        delegated.attribute('sub.sub2.sub3', 'attr1', '')
        call_test = delegated.attribute('sub.sub2.call_test()', 'attr1')
        deep_call_test = delegated.attribute('sub.sub2.sub3.call_test().call_sub', 'attr1')
        attr2 = delegated.attribute('sub.sub2.sub3.sub4', 'attr2')
        attr3, attr4 = delegated.attributes('sub.sub2', ['attr3', 'attr1'])

    m = Master()

    assert m.attr1 == m.sub.sub2.sub3.attr1
    m.attr1 = 'test'
    assert m.attr1 == 'test'
    assert m.attr1 == m.sub.sub2.sub3.attr1

    assert m.attr2 == m.sub.sub2.sub3.sub4.attr2
    m.attr2 = 'test'
    assert m.attr2 == 'test'
    assert m.attr2 == m.sub.sub2.sub3.sub4.attr2

    assert m.attr3 == m.sub.sub2.attr3
    m.attr3 = 'test'
    assert m.attr3 == 'test'
    assert m.attr3 == m.sub.sub2.attr3

    assert m.attr4 == m.sub.sub2.attr1
    m.attr4 = 'test'
    assert m.attr4 == 'test'
    assert m.attr4 == m.sub.sub2.attr1

    assert m.call_test == m.sub.sub2.call_test().attr1
    m.call_test = 'test'
    assert m.call_test == 'test'
    assert m.call_test == m.sub.sub2.call_test().attr1

    assert m.call_test == m.sub.sub2.sub3.call_test().call_sub.attr1
    m.call_test = 'test'
    assert m.call_test == 'test'
    assert m.call_test == m.sub.sub2.sub3.call_test().call_sub.attr1


def test_nested_method():
    class nested_call_helper(Subordinate):
        call_sub = Subordinate()
        def call_test(self):
            return self.call_sub

    class deep_nested_helper(Subordinate):
        deep_call_sub = nested_call_helper()
        def call_test(self):
            return self.deep_call_sub

    class Master():
        def __init__(self):
            self.sub = Subordinate()
            self.sub.sub2 = nested_call_helper()
            self.sub.sub2.sub3 = deep_nested_helper()
            self.sub.sub2.sub3.sub4 = Subordinate()
        delegated.method('sub.sub2.sub3.sub4', 'method1', '')
        call_test_method = delegated.method('sub.sub2.call_test()', 'method1')
        deep_call_test_method = delegated.method('sub.sub2.sub3.call_test().call_sub', 'method1')

        @delegated('sub.sub2')
        def method2(self): pass

        @delegated('sub.sub2.sub3', 'method1')
        def sub3_method1(self): pass

        method4 = delegated.method('sub.sub2', 'method2')
        method5, method6 = delegated.methods('sub.sub2.sub3', ['method3', 'method1'])

    m = Master()
    assert m.method1 == m.sub.sub2.sub3.sub4.method1
    assert m.method2 == m.sub.sub2.method2
    assert m.sub3_method1 == m.sub.sub2.sub3.method1
    assert m.method4 == m.sub.sub2.method2
    assert m.method5 == m.sub.sub2.sub3.method3
    assert m.method6 == m.sub.sub2.sub3.method1
    assert m.call_test_method == m.sub.sub2.call_test().method1
    assert m.deep_call_test_method == m.sub.sub2.sub3.call_test().call_sub.method1
