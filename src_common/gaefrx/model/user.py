'''
    User
        * lookup :
            - by email

Created on Jun 24, 2015

@author: jldupont
'''

from google.appengine.ext import ndb

from custom import DbResource, DomainKeyProperty, RolesProperty #UserKeyProperty

class FederatedIdentity(ndb.Model):
    '''
    The model for third party federated identities
    e.g. Google, Facebook
    
    The properties 'user_id' and 'token' shall be considered opaque 
    '''
    
    SUPPORTED_REALMS = ['google', ]
    
    realm      = ndb.StringProperty(choices = SUPPORTED_REALMS, required = True)
    user_id    = ndb.StringProperty(default = '')
    email      = ndb.StringProperty(required = True)
    token      = ndb.StringProperty(required = True)
    

class User(DbResource):
    '''
    The User datastore model
    
    A user can only belong to 1 domain
    '''
    domain = DomainKeyProperty(default = None)
    
    name_first = ndb.StringProperty(default='')
    name_last  = ndb.StringProperty(default='')
    email      = ndb.StringProperty(repeated = True)
    
    identities = ndb.StructuredProperty(FederatedIdentity, repeated = True)

    roles = RolesProperty(default=[])
    
    def get_identity_by_realm(self, realm):
        '''
        @return FederatedIdentity | None
        '''
        assert isinstance(realm, basestring), "Expected string, got: %s" % repr(realm)
        
        realm = realm.lower()
        
        for ident in self.identities:
            _realm = ident.realm.lower()
            if _realm == realm:
                return ident
            
        return None
            
        