'''
    API - Domain resource
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

import setup #@UnusedImport

#from gaefrx.excepts import BadRequestError, NotFoundError

from gaefrx.api.base import BaseApi
from gaefrx.api.response import ApiResponse
import gaefrx.api.code as code

import gaefrx.data.user as user

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
    """
    #def hget(self, *p):
    #    logging.info("Domain, GET: %s" % (p, ))

class ApiUserAdmin(BaseApi):
    """
    The API for the resource 'User/Admin'
    """
    def hpost(self):
        '''
        Create Admin user
        '''
        user.assign_admin()
        return ApiResponse(code.SUCCESS, [])


app = webapp2.WSGIApplication([
                                ('/_api/user',           ApiUserCollection)
                               ,('/_api/user/admin',     ApiUserAdmin)
                               ,('/_api/user/(.*)',      ApiUser)
                               ])
