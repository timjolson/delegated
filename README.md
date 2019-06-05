# delegated
python3 decorator, method proxy, attribute proxy to delegate tasks to a sub-object

    delegated.attr_proxy  # property object, allows access to another object's attribute
    delegated.method_proxy  # property method, allows access to another object's method

    from delegated import delegated
    delegated  # class, use as method decorator
    
    # methods
    delegated.attribute   # returns attr_proxy
    delegated.attributes  # returns [attr_proxy, ...]
    delegated.method      # returns method_proxy
    delegated.methods     # returns [method_proxy, ...]


Use the decorator inside a class definition

    @delegated('name_of_sub_component')
    def same_name_as_sub_component_method(self): pass
    
    @delegated('name_of_sub_component', 'name_of_sub_component_method')
    def whatever_method_name(self): pass
    

Main usage case:

    from delegated import delegated
    
    class Sub():
        '''Subordinate class'''
        attr1 = 1    
        ...   
        attr99 = 99
        
        def method1(self, *args, **kwargs): pass
        ...
        def method99(self, *args, **kwargs): pass
    
    class Master():
        '''Class or instance attributes and methods are supported'''
        sub = Sub()
        def __init__(self):
            self.instance_sub = Sub()
    
    class ImplicitMaster(Master):
        """Implicit delegation is simplest. Note: need '' final parameter
        to automatically apply the delegation to the class."""
        delegated.attributes('sub', 'attr1 attr2, ..., attr99', '')
        delegated.methods('sub', 'method1, method2, ..., method99', '')

    class ExplicitMaster(Master):
        '''Explicit delegation allows for renaming and code completion for methods and attrs.'''
        attr1, ..., attr99 = delegated.attributes('sub', 'attr1, ..., attr99')
        method1, ..., method99 = delegated.methods('sub', 'method1, ..., method99')

    class DecoratedMaster(Master):
        """Decorating allows for renaming and code completion for methods.
        Note: defined methods' parameter structure is ignored"""
        # simple
        @delegated('sub')
        def method1(self):pass
        
        # renaming
        @delegated('sub', 'method69')
        def best_method(self):pass


Additional usage:

    # already instantiated objects can be used (always the same object, 
    # instead of dynamic or instance-base)

    class Master(Master):
        sub = Sub()

        @delegated(sub)
        def method1(self): pass
        
        @delegated(sub, 'method2')
        def class_object_method(self): pass

        method3 = delegated.method(sub, 'method3')
        attr1 = delegated.attribute(sub, 'attr1')
