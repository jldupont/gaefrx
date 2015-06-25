'''
Created on Jun 24, 2015

@author: jldupont
'''
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from pyrbac import Admin, Guest
from gaefrx.model.custom import RolesProperty


class TestEntity(ndb.Model):
    
    roles = RolesProperty()


class Test(unittest.TestCase):


    def setUp(self):
        self.testbed = testbed.Testbed()
        
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()        


    def tearDown(self):
        self.testbed.deactivate()


    def testRolesProperty1(self):
        '''
        Just test the custom property
        '''
        roles = [Admin, Guest]
        
        te = TestEntity()
        te.roles = roles
        
        self.assertTrue(Admin in te.roles)
        self.assertTrue(Guest in te.roles)


    def testRolesProperty2(self):
        '''
        Test the serialization / deserialization capability of the custom property
        '''
        roles = [Admin, Guest]
        
        te = TestEntity()
        te.roles = roles
        
        te.put()
        
        entities = TestEntity.query().fetch(2)
        
        self.assertEqual(1, len(entities))
        
        te2 = entities[0]
        
        self.assertTrue(Admin in te2.roles)
        self.assertTrue(Guest in te2.roles)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()