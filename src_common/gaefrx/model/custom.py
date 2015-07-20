'''
Custom Property Definitions

Used mainly as helpers for static type checking

Created on Jun 24, 2015

@author: jldupont
'''
import json

from google.appengine.ext import ndb

from pyrbac import Resource, Role, roles_class_to_name_list, roles_class_from_name_list


class DbResource(Resource, ndb.Model):
    '''
    Generic Datastore Resource
    
    We use as a base the class 'Resource' from pyrbac
     in order to enforce access control 
    '''
    created_by       = ndb.KeyProperty()
    last_modified_by = ndb.KeyProperty()
    date_created     = ndb.DateTimeProperty(auto_now_add=True)
    date_accessed    = ndb.DateTimeProperty(auto_now=True)
    suspended        = ndb.BooleanProperty(default=False)

    def to_dict_for_export(self):
        return self.to_dict(exclude = ['date_created', 'date_accessed', 
                                       'created_by', 'last_modified_by'] )


class UserKeyProperty(ndb.KeyProperty):
    pass

class DomainKeyProperty(ndb.KeyProperty):
    pass

class RolesProperty(ndb.StringProperty):
    '''
    For representing access control Roles
    
    This property consists of a list of Role classes
    @see pyrbac.role
    '''
    def _validate(self, value):
        if not isinstance(value, list):
            raise TypeError('expected a list, got %s' % repr(value))
        
        if not all(issubclass(elem, Role) for elem in value):
            raise TypeError('expected a List of Role, got %s' % repr(value))
    
    def _to_base_type(self, value):
        
        names_list = self.to_json(value)
        return json.dumps(names_list)
    
    def _from_base_type(self, value):
        '''
        We expect to be receiving a JSON list of strings
        '''
        names_list = json.loads(value)
        return roles_class_from_name_list(names_list) 

    @classmethod
    def to_json(cls, value):
        return roles_class_to_name_list(value)
    