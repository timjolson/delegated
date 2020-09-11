# delegated

## Python3 Class to delegate tasks to a subordinate object.
Create proxies to methods or attributes via decorator, assignment, or automatic class embedding. 

Subordinates can be an existing object, or the name of an instance//class attribute to be dynamically retrieved.

Supervisor can be a class instance, or a dict (keys are used as attribute names).

---

#### Create proxies to methods or attributes via decorator, assignment, or automatic class embedding. 

    class delegated(object):
        def tasks       # Delegates attribute(s) and returns their proxies.
        def here        # Delegates attribute(s) and embeds into the containing class.
        
        # For .tasks and .here, the subordinate attribute names can be: 
        # a sequence of strings:  ['name1', 'name2', ...]
        # OR 
        # a single comma//space separated string: 'name1, name2, name3' // 'name1 name2 name3'

#### Base classes for the README examples:
    
    class Sub():
        '''Subordinate class (helper for following examples).'''
        attr1 = 1    
        ...   
        attr99 = 99
        
        def method1(self, *args, **kwargs): pass
        ...
        def method99(self, *args, **kwargs): pass
    
    class Master():
        '''Base class for following examples.
        Subordinate objects can be class or instance attributes.'''
        sub = Sub()  # class attribute
        def __init__(self):
            self.instance_sub = Sub()  # instance attribute


#### Delegate via assignment:
    # Explicit delegation allows for renaming and some code completion.
    class ExplicitMaster(Master):
        attr1, ..., attr99 = delegated.tasks(sub, 'attr1, ..., attr99')
        method1, ..., method99 = delegated.tasks('sub', 'method1, ..., method99')


#### Delegate via class embedding:
    # Implicit delegation is simplest, but has least options.
    class ImplicitMaster(Master):
        delegated.here('sub', 'attr1 attr2 ... attr99')
        delegated.here(sub, 'method1, method2, ..., method99')


#### Delegate via decorator
    #Decorating allows for renaming and some code completion.
    #Note: The defined methods' signature (parameters, etc.) is irrelevant.
    #      It may be useful, however, for reference."""
    
    class DecoratedMaster(Master):
        ...
        # keep method name, use `sub` object's `method1`
        @delegated('sub')
        def method1(self):
            pass

        # OR
        
        # rename, use `instance_sub.method1` under name `best_method`
        @delegated('instance_sub', 'method1')
        def best_method(self):
            pass
        
        # NOTE: Like assignment or embedding, decorating can also 
        # accept object subordinates instead of strings
        @delegated(sub)
        def method1(self):
            pass
        ...


#### Advanced usage:

    # Nested methods/attributes can be specified
    method = delegate.tasks('sub.sub2.sub3', 'method_name')
    delegate.here('sub.sub2.sub3', 'method_name')

    # Basic functions (no args) can be called to acquire deeper objects
    method = delegate.tasks('sub.sub2.retriever()', 'method_name')
    delegate.here('sub.retriever().sub2', 'method_name')
