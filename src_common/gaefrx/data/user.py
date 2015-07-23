'''
Internal Data Access - User 

Created on Jul 9, 2015

@author: jldupont
'''
from pyrbac.role import Role, Admin

from gaefrx.model.user import User, FederatedIdentity
from gaefrx.excepts import DatastoreError, InvalidParameterValueError
from gaefrx.excepts import BadRequestError, NotFoundError

from gaefrx.data import isp as isp 


def ensure_authentication(context):
    """
    Verifies authentication status
    
    @param context: { name, email, token, realm }
    
    @return (True | False, user | None)
    @raise BadRequestError, NotFoundError
    """
    
    email = context.get('email', None)
    if email is None:
        raise BadRequestError('missing email')
    
    u = get_by_email(email)
    if u is None:
        raise NotFoundError('user')
    
    realm = context.get('realm', None)
    if realm is None:
        raise BadRequestError('realm')
    
    idp = u.get_identity_by_realm(realm)
    if idp is None:
        raise NotFoundError('realm identity')
    
    if idp.token == '' or idp.token is None:
        return (False, u)
    
    return (idp.token == context.get('token', None), u)
    
def save_token(user, realm, token):
    '''
    Just updates the token of a user
    
    The identity property must already exists
    
    @raise NotFoundError
    @raise DatastoreError
    '''
    assert isinstance(user, User)
    assert isinstance(realm, basestring)
    
    ident = user.get_identity_by_realm(realm)
    if ident is None:
        raise NotFoundError('identity')
    
    ident.token = token
    
    try:
        user.put()
    except:
        raise DatastoreError()
    

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
    
def create(realm = None, email = None, token = None, user_id = '', name_first = '', name_last = ''):
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
    
    if realm not in FederatedIdentity.SUPPORTED_REALMS:
        raise InvalidParameterValueError('realm')
    
    u = User(name_first = name_first, name_last = name_last
             ,email = [email]
             ,identities = [FederatedIdentity(realm = realm, user_id = user_id, email = email, token = token)]
             )
    try:
        u.put()
        
    except Exception, e:
        raise DatastoreError(e)
    
    return u
    

def assign_admin():
    '''
    Assign the role 'admin' to the first user created
    
    @raise DatastoreError
    @raise NotFoundError
    '''
    q = User.query()
    q = q.order(User.date_created)
    
    try:
        u = q.fetch(1)[0]
    except Exception, e:
        raise DatastoreError( e )
    
    add_role(u, Admin)

    try:
        u.put()
        
    except Exception, e:
        raise DatastoreError( e )
    
    
    
def add_role(user, role):
    '''
    Add 1 Role to user 
    '''
    assert isinstance(user, User), 'expecting User, got: %s' % repr(user)
    assert issubclass(role, Role), 'expecting Role, got: %s' % repr(user)
    
    if role not in user.roles:
        user.roles.append(role)
    
def update():
    '''
    '''
    
    
def delete():
    '''
    '''

#
# =====================
# 
def delete_sessions(u):
    '''
    Delete the session tokens for all identities
    
    @raise DatastoreError
    @return None
    '''
    assert isinstance(u, User), 'expected User, got: %s' % repr(u)
    
    for ident in u.identities:
        ident.token = None
   
    try:
        u.put()
        
    except Exception, e:
        raise DatastoreError(e)
    
#
# =====================
# 

def verify_identity_authentication(realm, token):
    '''
    Verify with the Identity Service Provider
     the validity of the authentication parameters
     
    @param realm : a supported realm (e.g. google, ... )
    @param token : a realm specific authentication token
    
    @return dict user_data
    @raise InvalidParameterValueError
    @raise RemoteServiceError
    @raise NotFoundError
    '''
    
    provider = isp.lookup_provider(realm)
    return provider.verify(token)
    
    