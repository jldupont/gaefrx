'''
Created on Jun 24, 2015

@author: jldupont
'''
from google.appengine.ext import ndb

from custom import DbResource


class Domain(DbResource):
    '''
    The Domain datastore model
    '''
    name = ndb.StringProperty(default='')
    
    
    def to_json(self):
        '''
        Prepare a JSON string representation
        '''
        return self.to_dict_for_export()
    