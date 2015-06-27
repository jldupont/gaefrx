'''
    API - Session resource
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

import setup #@UnusedImport

from gaefrx.api import BaseApi
from gaefrx.api.response import ApiResponse
import gaefrx.api.code as code


class ApiSession(BaseApi):
    
    def hpost(self, *p):
        '''
        Sign-In
        '''
        logging.info("Session:Sign-in: %s" % (p, ))
        
        return ApiResponse(code.SUCCESS, [])

    def hdelete(self, *p):
        '''
        Sign-Out
        '''
        logging.info("Session:Sign-out: %s" % (p, ))
        
        return ApiResponse(code.SUCCESS, [])




app = webapp2.WSGIApplication([
                                ('/_api/session',  ApiSession)
                               ])
