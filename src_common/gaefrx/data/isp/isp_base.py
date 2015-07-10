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
            
            name = cls.__name__.lower()
            newclass.name = name
            cls.isps[name] = newclass
    
        return newclass

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
    