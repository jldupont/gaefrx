'''
Created on Jun 24, 2015

@author: jldupont
'''

from google.appengine.ext import ndb

from custom import DbResource, DomainKeyProperty, RolesProperty #UserKeyProperty


class User(DbResource):
    '''
    The User datastore model
    
    A user can only belong to 1 domain
    '''
    domain = DomainKeyProperty()
    
    name_first = ndb.StringProperty(default='')
    name_last  = ndb.StringProperty(default='')

    roles = RolesProperty(default=[])
    