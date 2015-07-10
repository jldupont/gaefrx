'''
Created on Jul 9, 2015

@author: jldupont
'''

from gaefrx.excepts import NotFoundError

class MetaIsp(type):
    
    isps = {}
    
    def __new__(cls, future_class_name, future_class_parents, future_class_attr):
        newclass=super(MetaIsp, cls).__new__(cls, future_class_name, future_class_parents, future_class_attr)
        
        if newclass.__name__ != 'BaseIsp':
            cls._register_class(newclass)
        return newclass
    
    @classmethod
    def _register_class(cls, klass):
        '''
        Register a BaseISP subclass
        
        This method can be used for mock based tests
        
        @return klass
        '''
        assert issubclass(klass, BaseIsp), "Expected subclass of BaseIsp, got: %s" % repr(klass)
       
        name = klass.__name__.lower()
        
        if not name.startswith('isp'):
            raise Exception('Providers must start with "Isp"')
        
        realm_name = name[3:]
        
        cls.isps[realm_name] = klass
        klass.name = realm_name
        return klass
        

class BaseIsp():
    
    __metaclass__ = MetaIsp
    
    def verify(self, email, token):
        raise Exception('unimplemented')
    

def lookup_provider(name):
    '''
    @param name: the isp name
    @return BaseIsp subclass
    @raise  NotFoundError
    '''
    assert isinstance(name, basestring), 'expected string, got: %s' % repr(name)
    try:
        return MetaIsp.isps[name]
    except:
        raise NotFoundError('realm: %s' % repr(name))
    