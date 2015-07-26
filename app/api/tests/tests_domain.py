'''
Created on Jul 26, 2015

@author: jldupont

Ref:  http://webapp-improved.appspot.com/guide/testing.html 

'''
import os
import json
import unittest
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from pyrbac import Admin

from api import setup

import gaefrx.data.user as duser
from api.api_domain import app

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
        
        d = {'realm':      'google'
             ,'email':     'test@example.com'
             ,'token':     '6666'
             ,'user_id':    'id'
             ,'name_first': 'first'
             ,'name_last':  'last'
             ,'roles': [ Admin ]
             }
        self.u = duser.create(**d)     
        
        
        requires_permission._DEBUG = True
        
        

    def tearDown(self):
        self.testbed.deactivate()

    def _create_domain(self):
        
        request = webapp2.Request.blank('/_api/domain/testdomain'
                                        ,headers={
                                                  'From': 'test@example.com'
                                                  ,'X-email': 'test@example.com'
                                                  ,'X-realm': 'google'
                                                  ,'X-token': '6666'
                                                  }
                                        )
        request.method = 'POST'
        
        # Get a response for that request.
        return request.get_response(app)
        


    def test_domain_create(self):
        
        # Get a response for that request.
        response = self._create_domain()

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200, 'got: %s' % response)
        

    def test_domain_read(self):
        
        # Get a response for that request.
        self._create_domain()

        request = webapp2.Request.blank('/_api/domain/testdomain'
                                        ,headers={
                                                  'From': 'test@example.com'
                                                  ,'X-email': 'test@example.com'
                                                  ,'X-realm': 'google'
                                                  ,'X-token': '6666'
                                                  }
                                        )
        request.method = 'GET'

        response = request.get_response(app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200, 'got: %s' % response)
        
        jrepr = json.loads( response.body )
        
        self.assertEqual(jrepr['name'], 'testdomain', 'got: %s' % response)
        
       