'''
Created on Jun 24, 2015

@author: jldupont
'''

from google.appengine.ext import ndb

from pyrbac import Resource

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


class User(DbResource):
    '''
    The generic User class
    '''
    