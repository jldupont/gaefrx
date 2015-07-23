'''
Internal Data Access - User 

Created on Jul 9, 2015

@author: jldupont
'''

from gaefrx.model.domain import Domain
from gaefrx.excepts import DatastoreError#, InvalidParameterValueError
#from gaefrx.excepts import BadRequestError, NotFoundError



def get_by_name(name):
    '''
    Lookup a Domain
    
    @param name
    
    @return Domain | None
    @raise DatastoreError
    '''
    assert isinstance(name, basestring), 'Excepting string, got: %s' % repr(name)
    
    q = Domain.query( Domain.name == name )
    
    try:
        d = q.get()
        
    except Exception, e:
        raise DatastoreError(e)

    return d
    
def create(name = None):
    '''
    Create a Domain entity
    
    Duplicates are possible - check for existence prior to using this method
    
    @param name:
    
    @return Domain
    
    @raise DatastoreError
    '''
    assert isinstance(name, basestring), 'Expected string, got: %s' % repr(name)
    
    d = Domain(name = name)
    
    try:
        d.put()
        
    except Exception, e:
        raise DatastoreError(e)
    
    return d
    
    
def update():
    '''
    '''
    
    
def delete():
    '''
    '''

#
# =====================
# 
    
#
# =====================
# 

