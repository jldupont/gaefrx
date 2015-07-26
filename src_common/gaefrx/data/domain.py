'''
Internal Data Access - User 

Created on Jul 9, 2015

@author: jldupont
'''

from gaefrx.model.domain import Domain
from gaefrx.excepts import DatastoreError#, InvalidParameterValueError
#from gaefrx.excepts import BadRequestError, NotFoundError

def export_domain(collection):
    '''
    Prepares a collection for export to JSON
    
    @param collection: [Domain, ...]
    @return: [dict, ... ]
    '''
    assert isinstance(collection, list)
    
    return [domain.to_json() for domain in collection]
    

def read_page(cursor = None, count = 100):
    '''
    Retrieve a page worth of domain(s)
    
    @param cursor : an 'url safe' cursor or None
    
    @return (domains, next_cursor, more)
    '''
    
    if count is None:
        count = 100
    
    q = Domain.query()
    
    q = q.order(Domain.name)
    
    #
    # If nothing can be found,
    #  domains = []
    #  cursor = None
    #
    domains, maybe_next_cursor, more = q.fetch_page(count, start_cursor = cursor)
    
    if maybe_next_cursor is None:
        next_cursor = None
    else:
        next_cursor = maybe_next_cursor.urlsafe()
    
    return (domains, next_cursor, more)



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

