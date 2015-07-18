'''
Created on Jul 10, 2015

@author: jldupont
'''
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import gaefrx.setup_secrets #@UnusedImport

import gaefrx.data.isp as isp
import gaefrx.data.user as user

from gaefrx.excepts import BadRequestError, NotFoundError

class Test1(unittest.TestCase):


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


    def testIspBase1(self):
        
        i1 = isp.IspGoogle()
        
        self.assertTrue(i1.name, 'google')
        
    def testIspBase2(self):
        
        provider = isp.lookup_provider('google')
        
        self.assertTrue(issubclass(provider, isp.BaseIsp))
        
    def testDataUserBase1(self):
        
        u = user.get_by_email('email@test.com')
        
        self.assertEqual(u, None, 'Expecting None')
        
    def testDataUserCreation(self):
        
        u = user.create( realm = 'google', email = 'email@test.com', token = "6666")
        
        self.assertTrue(isinstance(u, user.User), 'Expecting a User entity')

        uf = user.get_by_email('email@test.com')
        
        uf_i1 = uf.identities[0]
        
        self.assertTrue(uf_i1.realm, 'google')
        self.assertTrue(uf_i1.token, '6666')
        
        uf_i2 = uf.get_identity_by_realm('GOOgle')
        self.assertTrue(uf_i2.realm, 'google')
        self.assertTrue(uf_i2.token, '6666')
        
        uf_i3 = uf.get_identity_by_realm('FACEBOOK')
        self.assertEqual(uf_i3, None)


class Test2(unittest.TestCase):


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

        self.email = 'email@test.com'
        self.token = '6666'

        u = user.User(email = [self.email],
                      identities = [user.FederatedIdentity(
                                                           email = self.email
                                                           ,token = self.token
                                                           ,realm = 'google'
                                                           )]
                      )

        u.put()


    def tearDown(self):
        self.testbed.deactivate()


    def testEnsureAuth1(self):

        result, _ = user.ensure_authentication({
                                              'email':  self.email
                                             ,'token':  self.token
                                             ,'realm':  'google'
                                             })
        
        self.assertTrue(result, 'Expecting True')

    def testEnsureAuth2(self):

        def raises():
            user.ensure_authentication({
                                                  'email':  None
                                                 ,'token':  self.token
                                                 ,'realm':  'google'
                                                 })
        
        self.assertRaises(BadRequestError, raises)

    def testEnsureAuth3(self):

        def raises():
            user.ensure_authentication({
                                                  'email':  'unknown_email'
                                                 ,'token':  self.token
                                                 ,'realm':  'google'
                                                 })
        
        self.assertRaises(NotFoundError, raises)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()