'''
Internal Data Access - User 

Created on Jul 9, 2015

@author: jldupont
'''

from gaefrx.model.user import User, FederatedIdentity
from gaefrx.excepts import DatastoreError, InvalidParameterValueError #, ExistsError


def get_by_email(email):
    '''
    Lookup a User using the email property
    
    @param email
    
    @return User | None
    @raise DatastoreError
    '''
    assert isinstance(email, basestring), 'Excepting string, got: %s' % repr(email)
    
    q = User.query( User.email.IN([email]) )
    
    try:
        r = q.get()
        
    except Exception, e:
        raise DatastoreError(e)

    return r
    
def create(realm, email, token, user_id = '', name_first = '', name_last = ''):
    '''
    Create a User entity
    
    Duplicates are possible - check for existence prior to using this method
    
    @param realm:     a supported realm (e.g. google, facebook)
    @param email:     the email address
    @param token:     the realm specific token associated with this user
    @param user_id:   if available, the realm specific user_id
    @param name_first 
    @param name_last
    
    @return User
    
    @raise DatastoreError
    @raise InvalidParameterValueError
    '''
    assert isinstance(email, basestring), 'Expected string, got: %s' % repr(email)
    assert isinstance(token, basestring), 'Expected string, got: %s' % repr(token)
    
    if realm not in FederatedIdentity.realm:
        raise InvalidParameterValueError('realm')
    
    u = User(name_first = name_first, name_last = name_last
             ,email = email
             ,identities = FederatedIdentity(realm = realm, user_id = user_id, email = email, token = token)
             )
    try:
        u.put()
        
    except Exception, e:
        raise DatastoreError(e)
    
    return u
    
def update():
    '''
    '''
    
    
def delete():
    '''
    '''
   
#
# =====================
# 

def verify_identity_authentication(realm, email, token):
    '''
    Verify with the Identity Service Provider
     the validity of the authentication parameters
     
    @param realm : a supported realm (e.g. google, ... )
    @param email
    @param token : a realm specific authentication token
    
    @return True | False
    @raise InvalidParameterValueError
    @raise RemoteServiceError
    '''
    
    