'''
Created on Jul 25, 2015

@author: jldupont

Ref:  http://webapp-improved.appspot.com/guide/testing.html 

'''
import os
import unittest
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from pyrbac import Admin

from api import setup

import gaefrx.data.user as duser
from api.api_session import app

from gaefrx.api.base import requires_permission


class TestHandlers(unittest.TestCase):

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
        
        #
        #
        #
        
        #requires_permission._DEBUG = True
        
        d = {'realm':      'google'
             ,'email':     'test@example.com'
             ,'token':     '6666'
             ,'user_id':    'id'
             ,'name_first': 'first'
             ,'name_last':  'last'
             ,'roles': [ Admin ]
             }
        self.u = duser.create(**d)     

        

    def tearDown(self):
        self.testbed.deactivate()
        self.u = None


    def _attempt_delete(self):
        
        request = webapp2.Request.blank('/_api/session'
                                        ,headers={
                                                  'From': 'test@example.com'
                                                  ,'X-email': 'test@example.com'
                                                  ,'X-realm': 'google'
                                                  ,'X-token': '6666'
                                                  }
                                        )
        request.method = 'DELETE'
        
        # Get a response for that request.
        return request.get_response(app)
        

    def test_session_delete(self):
        '''
        We have an 'authenticated' session created in setUp
        
        Let's try to delete this a first time: OK
        A second time: Unauthorized
        '''
        response = self._attempt_delete()

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200, 'Expected 200, got: %s' % response)

        
        response2 = self._attempt_delete()

        # Let's check if the response is correct.
        self.assertEqual(response2.status_int, 403, 'Expected 403, got: %s' % response)
        
       