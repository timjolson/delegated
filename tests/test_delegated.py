import pytest
from delegated import delegated

# import logging
# logger = delegated.logger
# logger.addHandler(logging.FileHandler('test.log', 'w'))


class Subordinate():
    def __init__(self, depth=0):
        super(Subordinate).__init__()
        self.attr1 = f'attr1_{depth}'
        self.attr2 = f'attr2_{depth}'
        self.depth = depth
        self.sub = Subordinate(depth+1) if depth < 5 else None
    def method1(self, *args, **kwargs):
        return 'method1', self, self.depth, args, kwargs
    def method2(self, *args, **kwargs):
        return 'method2', self, self.depth, args, kwargs
    def call_test_class(self):
        return self.Sub
    def call_test_instance(self):
        return self.sub


Subordinate.Sub = Subordinate()


def check_attrs(m):
    assert m.attr1 is m.sub.attr1
    assert m.attr2 is m.sub.attr2
    assert m.attr3 is m.sub.attr1


def check_embed_attrs(m):
    assert m.attr1 is m.sub.attr1
    assert m.attr2 is m.sub.attr2


def check_methods(m):
    assert m.method1() == m.sub.method1()
    assert m.method2() == m.sub.method2()
    assert m.method3() == m.sub.method1()


def check_embed_methods(m):
    assert m.method1() == m.sub.method1()
    assert m.method2() == m.sub.method2()


def test_tasks_str_str():
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


def test_tasks_instance_str():
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


def test_tasks_str_str_instanceattr():
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

    check_embed_attrs(Master())

    class Master():
        sub = Subordinate()
        delegated.here('sub', 'attr1, attr2')
        delegated.here('sub', 'attr3')

    check_embed_attrs(Master())


def test_attrs_embed_instance_str():
    class Master():
        sub = Subordinate()
        delegated.here(sub, 'attr1')
        delegated.here(sub, 'attr2')

    check_embed_attrs(Master())

    class Master():
        sub = Subordinate()
        delegated.here(sub, 'attr1, attr2')
        delegated.here(sub, 'attr3')

    check_embed_attrs(Master())


def test_attrs_embed_str_str_instanceattr():
    class Master():
        def __init__(self):
            self.sub = Subordinate()

        delegated.here('sub', 'attr1')
        delegated.here('sub', 'attr2')

    check_embed_attrs(Master())

    class Master():
        def __init__(self):
            self.sub = Subordinate()

        delegated.here('sub', 'attr1, attr2')

    check_embed_attrs(Master())


def test_methods_embed_str_str():
    class Master():
        sub = Subordinate()
        delegated.here('sub', 'method1')
        delegated.here('sub', 'method2')

    check_embed_methods(Master())

    class Master():
        sub = Subordinate()
        delegated.here('sub', 'method1, method2')

    check_embed_methods(Master())


def test_methods_embed_instance_str():
    class Master():
        sub = Subordinate()
        delegated.here(sub, 'method1')
        delegated.here(sub, 'method2')

    check_embed_methods(Master())

    class Master():
        sub = Subordinate()
        delegated.here(sub, 'method1, method2')

    check_embed_methods(Master())


def test_methods_embed_str_str_instanceattr():
    class Master():
        def __init__(self):
            self.sub = Subordinate()

        delegated.here('sub', 'method1')
        delegated.here('sub', 'method2')

    check_embed_methods(Master())

    class Master():
        def __init__(self):
            self.sub = Subordinate()
        delegated.here('sub', 'method1, method2')

    check_embed_methods(Master())


def test_basics_multiple_instances():
    class Master():
        def __init__(self):
            self.sub = Subordinate()

        attr1 = delegated.tasks('sub', 'attr1')
        attr2 = delegated.tasks('sub', 'attr2')
        attr3 = delegated.tasks('sub', 'attr1')

        shared = Subordinate()  # class attr, shared between instances
        shared_attr = delegated.tasks('shared', 'attr1')

    m1, m2 = Master(), Master()

    check_attrs(m1)
    check_attrs(m2)

    m1.attr1 = 'changed m1'
    assert m1.attr1 != m2.attr1
    check_attrs(m1)

    m2.attr3 = 'changed m2'
    assert m1.attr1 != m2.attr1
    check_attrs(m2)

    m1.shared_attr = 'changed shared m1'
    assert m1.shared_attr is m2.shared_attr


def test_nested_tasks():
    class Master():
        Sub = Subordinate()
        def __init__(self):
            self.sub = Subordinate()
        delegated.here('Sub.sub.sub', 'attr1')
        attr1 = delegated.tasks('sub.sub.call_test_instance().call_test_class().sub', 'attr1')
        attr2, attr3 = delegated.tasks('sub.call_test_class().sub.call_test_instance().sub', 'attr2, attr1')
        method1, method2 = delegated.tasks(Sub.sub.call_test_class().sub, 'method1, method2')
        method3 = delegated.tasks(Sub.sub.call_test_instance().sub, 'method1')

    m = Master()

    assert m.attr1 is m.Sub.sub.call_test_instance().call_test_class().sub.attr1
    m.attr1 = 'test'
    assert m.attr1 is m.Sub.sub.call_test_instance().call_test_class().sub.attr1

    assert m.attr2 is m.Sub.call_test_class().sub.call_test_instance().sub.attr2
    m.attr2 = 'test'
    assert m.attr2 is m.Sub.call_test_class().sub.call_test_instance().sub.attr2

    assert m.attr3 is m.Sub.call_test_class().sub.call_test_instance().sub.attr1
    m.attr3 = 'test'
    assert m.attr3 is m.Sub.call_test_class().sub.call_test_instance().sub.attr1

    assert m.method1() == m.Sub.sub.call_test_class().sub.method1()
    assert m.method2() == m.Sub.sub.call_test_class().sub.method2()
    assert m.method3() == m.Sub.sub.call_test_instance().sub.method1()


def test_nested_here():
    class Master():
        def __init__(self):
            self.Sub = Subordinate()
        delegated.here('Sub.sub.sub', 'attr1')
        delegated.here('Sub.sub.call_test_instance().call_test_class().sub', 'attr1')
        delegated.here('Sub.call_test_class().sub.call_test_instance().sub', 'attr2, method1')

    m = Master()

    assert m.attr1 is m.Sub.sub.call_test_instance().call_test_class().sub.attr1
    m.attr1 = 'test'
    assert m.attr1 is m.Sub.sub.call_test_instance().call_test_class().sub.attr1

    assert m.attr2 is m.Sub.call_test_class().sub.call_test_instance().sub.attr2
    m.attr2 = 'test'
    assert m.attr2 is m.Sub.call_test_class().sub.call_test_instance().sub.attr2

    assert m.method1() == m.Sub.call_test_class().sub.call_test_instance().sub.method1()


def test_nested_decorated_here():
    class Master():
        def __init__(self):
            self.Sub = Subordinate()

        @delegated('Sub.call_test_instance().sub')
        def method1(self): pass

        @delegated('Sub.sub.call_test_class().sub', 'method2')
        def dec_method2(self): pass

        @delegated('Sub.sub.call_test_instance().call_test_class().sub', 'method1')
        def dec_method3(self): pass

    m = Master()

    assert m.method1() == m.Sub.call_test_instance().sub.method1()
    assert m.dec_method2() == m.Sub.sub.call_test_class().sub.method2()
    assert m.dec_method3() == m.Sub.sub.call_test_instance().call_test_class().sub.method1()


#TODO: build tests for Dict supervisor
#TODO: build tests for exceptions

