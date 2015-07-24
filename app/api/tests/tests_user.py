'''
Created on Jul 23, 2015

@author: jldupont

Ref:  http://webapp-improved.appspot.com/guide/testing.html 

'''
import unittest
import webapp2

from api.api_user import app

class TestHandlers(unittest.TestCase):
    
   def test_user_collection(self):
       
       request = webapp2.Request.blank('/_api/user')
       
       # Get a response for that request.
       response = request.get_response(app)

       # Let's check if the response is correct.
       self.assertEqual(response.status_int, 200)
       