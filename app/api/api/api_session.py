'''
    API - Session resource
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

import setup #@UnusedImport

from gaefrx.excepts import BadRequestError

from gaefrx.api import BaseApi#, requires_auth
from gaefrx.api.response import ApiResponse
import gaefrx.api.code as code
import gaefrx.data.user as user


class ApiSession(BaseApi):
    
    def hpost(self, *p):
        '''
        Sign-In
        
        @raise BadRequestError
        '''
        ctx = self.get_context()
        
        email = ctx['email']
        if email is None:
            raise BadRequestError('email') 
               
        maybe_user = user.get_by_email(email)
        
        #
        # 2 cases:
        #  a) user entity exists
        #  b) user entity must be created
        #

        
        return ApiResponse(code.SUCCESS, [])

    def hdelete(self, *p):
        '''
        Sign-Out
        '''
        logging.info("Session:Sign-out: %s" % (p, ))
        
        return ApiResponse(code.SUCCESS, [])


## -------------------------------------------------------

    def _create_user(self, ctx):
        '''
        Create the User entity given the request context
        
        @raise DatastoreError
        @raise InvalidParameterValueError
        @return User
        '''
        
        realm = ctx['realm']
        email = ctx['email']
        token = ctx['token']
        
        return user.create(realm, email, token)


app = webapp2.WSGIApplication([
                                ('/_api/session',  ApiSession)
                               ])
