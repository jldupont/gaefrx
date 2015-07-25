'''
    API - Domain resource
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

from pyrbac import Permission, Read
#from gaefrx.excepts import BadRequestError, NotFoundError

from gaefrx.api.base import BaseApi, requires_auth, requires_permission#, accept_parameters

from gaefrx.api.response import ApiResponse
import gaefrx.api.code as code

import gaefrx.data.user as duser

class ApiUserCollection(BaseApi):
    
    def hget(self, *p):
        '''
        Retrieve a list of users
        '''
        logging.info("User Collection, GET: %s" % (p, ))
        
        return ApiResponse(code.SUCCESS, [])



class ApiUser(BaseApi):
    """
    The API for the resource 'User'
    
    @raise NotFoundError
    """
    
    @requires_auth
    @requires_permission(Permission(duser.User, Read))
    def hget(self, _user, email):
        
        logging.info("Domain, GET: email: %s" % (email, ))
    
        u = duser.get_by_email(email)
        return ApiResponse(code.SUCCESS, u.to_json())


class ApiUserAdmin(BaseApi):
    """
    The API for the resource 'User/Admin'
    """
    
    def hpost(self):
        '''
        Create Admin user
        '''
        duser.assign_admin()
        return ApiResponse(code.SUCCESS, [])


app = webapp2.WSGIApplication([
                                ('/_api/user',           ApiUserCollection)
                               ,('/_api/user/admin',     ApiUserAdmin)
                               ,('/_api/user/(.*)',      ApiUser)
                               ])
