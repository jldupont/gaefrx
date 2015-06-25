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


    def testRolesProperty(self):
        
        roles = [Admin, Guest]
        
        te = TestEntity()
        te.roles = roles
        
        te.put()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()