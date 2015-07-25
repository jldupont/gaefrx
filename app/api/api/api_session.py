'''
    API - Session resource
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

from gaefrx.excepts import BadRequestError, NotFoundError

from gaefrx.api.base import BaseApi
from gaefrx.api.response import ApiResponse
import gaefrx.api.code as code 
import gaefrx.data.user as user

class ApiSession(BaseApi):
    
    def hpost(self, *p):
        '''
        Sign-In
        
        @raise BadRequestError
        @raise InvalidParameterValueError
        @raise RemoteServiceError
        @raise NotFoundError
        '''
        ctx = self.get_context()
        
        realm = ctx['realm']
        if realm is None:
            raise BadRequestError('realm')
        
        token = ctx['token']
        if token is None:
            raise BadRequestError('token')
        
        email = ctx['email']
        if email is None:
            raise BadRequestError('email') 
               
        maybe_user = user.get_by_email(email)
        
        #
        # 2 cases:
        #  a) user entity exists
        #  b) user entity must be created
        #
        
        if maybe_user is None:
            
            user_data = user.verify_identity_authentication(realm, token)
            
            user_data.pop('domain', None)
            user_data['realm'] = realm
            
            u = user.create(**user_data)
            
        else:
            _ = user.verify_identity_authentication(realm, token)
            u = maybe_user
            user.save_token(u, realm, token)
        
        return ApiResponse(code.SUCCESS, u)

    def hdelete(self, *p):
        '''
        Sign-Out
        
        @raise DatastoreError
        @raise NotFoundError
        '''
        #        @TODO:  Prevent third-party from delete session
        #                Currently, only the email address is required 
        

        ctx = self.get_context()
        
        email = ctx['email']
        if email is None:
            raise BadRequestError('email') 
        
        maybe_user = user.get_by_email(email)
        
        if maybe_user is None:
            raise NotFoundError()
        
        user.delete_sessions(maybe_user)
        
        return ApiResponse(code.SUCCESS, [])




app = webapp2.WSGIApplication([
                                ('/_api/session',  ApiSession)
                               ])
