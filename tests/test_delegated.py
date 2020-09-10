import pytest
from delegated import delegated


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
    assert isinstance(m.attr1, str)
    assert isinstance(m.attr2, str)
    assert isinstance(m.attr3, str)
    check_attr1(m)
    check_attr2(m)
    check_attr3(m)


def test_attributes_str_str():
    class Master():
        sub = Subordinate()
        attr1 = delegated.tasks('sub', 'attr1')
        attr2 = delegated.tasks('sub', 'attr2')
        attr3 = delegated.tasks('sub', 'attr1')

    check_attrs(Master())

    class Master():
        sub = Subordinate()
        attr1, attr2 = delegated.tasks('sub', 'attr1 attr2')
        attr3 = delegated.tasks('sub', 'attr1')

    check_attrs(Master())


def test_attributes_instance_str():
    class Master():
        sub = Subordinate()
        attr1 = delegated.tasks(sub, 'attr1')
        attr2 = delegated.tasks(sub, 'attr2')
        attr3 = delegated.tasks(sub, 'attr1')

    check_attrs(Master())

    class Master():
        sub = Subordinate()
        attr1, attr2 = delegated.tasks(sub, 'attr1 attr2')
        attr3 = delegated.tasks(sub, 'attr1')

    check_attrs(Master())


def test_attributes_str_str_instanceattr():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        attr1 = delegated.tasks('sub', 'attr1')
        attr2 = delegated.tasks('sub', 'attr2')
        attr3 = delegated.tasks('sub', 'attr1')

    check_attrs(Master())

    class Master():
        def __init__(self):
            self.sub = Subordinate()
        attr1, attr2 = delegated.tasks('sub', 'attr1 attr2')
        attr3 = delegated.tasks('sub', 'attr1')

    check_attrs(Master())


def test_methods_str_str():
    # TODO: remove duplicates now that there's only 1 type of proxy
    class Master():
        sub = Subordinate()
        method1 = delegated.tasks('sub', 'method1')
        method2 = delegated.tasks('sub', 'method2')
        method3 = delegated.tasks('sub', 'method1')

    check_methods(Master())

    class Master():
        sub = Subordinate()
        method1, method2 = delegated.tasks('sub', 'method1 method2')
        method3 = delegated.tasks('sub', 'method1')

    check_methods(Master())


def test_methods_instance_str():
    class Master():
        sub = Subordinate()
        method1 = delegated.tasks(sub, 'method1')
        method2 = delegated.tasks(sub, 'method2')
        method3 = delegated.tasks(sub, 'method1')

    check_methods(Master())

    class Master():
        sub = Subordinate()
        method1, method2 = delegated.tasks(sub, ['method1', 'method2'])
        method3 = delegated.tasks(sub, 'method1')

    check_methods(Master())


def test_methods_str_str_instanceattr():
    class Master():
        def __init__(self):
            self.sub = Subordinate()
        method1 = delegated.tasks('sub', 'method1')
        method2 = delegated.tasks('sub', 'method2')
        method3 = delegated.tasks('sub', 'method1')

    check_methods(Master())

    class Master():
        def __init__(self):
            self.sub = Subordinate()
        method1, method2 = delegated.tasks('sub', 'method1 method2')
        method3 = delegated.tasks('sub', 'method1')

    check_methods(Master())


def test_decorator_str_str():
    class Master():
        sub = Subordinate()

        @delegated('sub')
        def method1(self, *args, **kwargs): pass
        @delegated('sub')
        def method2(self, *args, **kwargs): pass
        @delegated('sub', 'method1')
        def method3(self, *args, **kwargs): pass

    check_methods(Master())


def test_decorator_instance_str():
    class Master():
        sub = Subordinate()

        @delegated(sub)
        def method1(self, *args, **kwargs): pass
        @delegated(sub)
        def method2(self, *args, **kwargs): pass
        @delegated(sub, 'method1')
        def method3(self, *args, **kwargs): pass

    check_methods(Master())


def test_decorator_str_str_instanceattr():
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


def test_attrs_embed_str_str():
    class Master():
        sub = Subordinate()
        delegated.here('sub', 'attr1')
        delegated.here('sub', 'attr2')

    check_attr1(Master())
    check_attr2(Master())

    class Master():
        sub = Subordinate()
        delegated.here('sub', 'attr1, attr2')

    check_attr1(Master())
    check_attr2(Master())


def test_attrs_embed_instance_str():
    class Master():
        sub = Subordinate()
        delegated.here(sub, 'attr1')
        delegated.here(sub, 'attr2')

    check_attr1(Master())
    check_attr2(Master())

    class Master():
        sub = Subordinate()
        delegated.here(sub, 'attr1, attr2')

    check_attr1(Master())
    check_attr2(Master())


def test_attrs_embed_str_str_instanceattr():
    class Master():
        def __init__(self):
            self.sub = Subordinate()

        delegated.here('sub', 'attr1')
        delegated.here('sub', 'attr2')

    check_attr1(Master())
    check_attr2(Master())

    class Master():
        def __init__(self):
            self.sub = Subordinate()

        delegated.here('sub', 'attr1, attr2')

    check_attr1(Master())
    check_attr2(Master())


def test_methods_embed_str_str():
    class Master():
        sub = Subordinate()
        delegated.here('sub', 'method1')
        delegated.here('sub', 'method2')

    check_method1(Master())
    check_method2(Master())

    class Master():
        sub = Subordinate()
        delegated.here('sub', 'method1, method2')

    check_method1(Master())
    check_method2(Master())


def test_methods_embed_instance_str():
    class Master():
        sub = Subordinate()
        delegated.here(sub, 'method1')
        delegated.here(sub, 'method2')

    check_method1(Master())
    check_method2(Master())

    class Master():
        sub = Subordinate()
        delegated.here(sub, 'method1, method2')

    check_method1(Master())
    check_method2(Master())


def test_methods_embed_str_str_instanceattr():
    class Master():
        def __init__(self):
            self.sub = Subordinate()

        delegated.here('sub', 'method1')
        delegated.here('sub', 'method2')

    check_method1(Master())
    check_method2(Master())

    class Master():
        def __init__(self):
            self.sub = Subordinate()
        delegated.here('sub', 'method1, method2')

    check_method1(Master())
    check_method2(Master())


def test_basics_multiple_instances():
    class Master():
        def __init__(self):
            self.sub = Subordinate()

        attr1 = delegated.tasks('sub', 'attr1')
        attr2 = delegated.tasks('sub', 'attr2')
        attr3 = delegated.tasks('sub', 'attr1')

        shared = Subordinate()
        shared_attr = delegated.tasks('shared', 'attr1')

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


def test_nested_attributes():
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
        delegated.here('sub.sub2.sub3', 'attr1')
        call_test = delegated.tasks('sub.sub2.call_test()', 'attr1')
        deep_call_test = delegated.tasks('sub.sub2.sub3.call_test().call_sub', 'attr1')
        attr2 = delegated.tasks('sub.sub2.sub3.sub4', 'attr2')
        attr3, attr4 = delegated.tasks('sub.sub2', ['attr3', 'attr1'])

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


def test_nested_methods():
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
        delegated.here('sub.sub2.sub3.sub4', 'method1')
        call_test_method = delegated.tasks('sub.sub2.call_test()', 'method1')
        deep_call_test_method = delegated.tasks('sub.sub2.sub3.call_test().call_sub', 'method1')

        @delegated('sub.sub2')
        def method2(self): pass

        @delegated('sub.sub2.sub3', 'method1')
        def sub3_method1(self): pass

        method4 = delegated.tasks('sub.sub2', 'method2')
        method5, method6 = delegated.tasks('sub.sub2.sub3', ['method3', 'method1'])

    m = Master()
    assert m.method1 == m.sub.sub2.sub3.sub4.method1
    assert m.method1() == m.sub.sub2.sub3.sub4.method1()
    assert m.method2 == m.sub.sub2.method2
    assert m.method2() == m.sub.sub2.method2()
    assert m.sub3_method1 == m.sub.sub2.sub3.method1
    assert m.sub3_method1() == m.sub.sub2.sub3.method1()
    assert m.method4 == m.sub.sub2.method2
    assert m.method4() == m.sub.sub2.method2()
    assert m.method5 == m.sub.sub2.sub3.method3
    assert m.method5() == m.sub.sub2.sub3.method3()
    assert m.method6 == m.sub.sub2.sub3.method1
    assert m.method6() == m.sub.sub2.sub3.method1()
    assert m.call_test_method == m.sub.sub2.call_test().method1
    assert m.call_test_method() == m.sub.sub2.call_test().method1()
    assert m.deep_call_test_method == m.sub.sub2.sub3.call_test().call_sub.method1
    assert m.deep_call_test_method() == m.sub.sub2.sub3.call_test().call_sub.method1()


#TODO: build tests for Dict
