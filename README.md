# delegated

## Python3 Class to delegate tasks to a subordinate object.
Create proxies to methods or attributes via decorator, assignment, or automatic class embedding. 

Subordinates can be an existing object, or the name of an instance//class attribute to be dynamically retrieved.

---

### Sample usage

    class Master(object):
        # Delegate explicitly
        attr1, ..., attr99 = delegated.tasks(sub, 'attr1, ..., attr99')  # the subordinate can be an existing object
        method1, ..., method99 = delegated.tasks('sub', 'method1, ..., method99')  # OR a string to use dynamic discovery
        
        # Delegate implicitly
        delegated.here('sub', 'attr1 ... attr99')
        delegated.here(sub, 'method1, ..., method99')
        
        # Delegate by decorating
        @delegated('sub')  # keep method name, use `sub` object's `method1`
        def method1(self):
            pass
        
        @delegated('instance_sub', 'method1')  # rename, use `instance_sub.method1` under name `best_method`
        def best_method(self):
            pass
        
        @delegated(sub)  # subordinate can be an object when decorating, too
        def method1(self):
            pass

        # The subordinate attribute names can be: 
        # a sequence of strings:  ['name1', 'name2', ...]
        # OR 
        # a single comma//space separated string: 'name1, name2, name3' // 'name1 name2 name3'


### Advanced usage:

    # Nested methods/attributes can be specified
    method = delegate.tasks('sub.sub2.sub3', 'method_name')
    delegate.here('sub.sub2.sub3', 'method_name')

    # Basic functions (no args) can be called to acquire deeper objects
    method = delegate.tasks('sub.sub2.retriever()', 'method_name')
    delegate.here('sub.retriever().sub2', 'method_name')
