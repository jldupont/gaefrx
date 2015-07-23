'''
    API - Domain resource
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

import setup #@UnusedImport

from gaefrx.api.base import BaseApi, requires_auth
from gaefrx.api.response import ApiResponse
import gaefrx.api.code as code


class ApiDomainCollection(BaseApi):
    
    def hget(self, *p):
        '''
        Retrieve a list of domains
        '''
        logging.info("Domain Collection, GET: %s" % (p, ))
        
        return ApiResponse(code.SUCCESS, [])



class ApiDomain(BaseApi):
    """
    The API for the resource 'Domain'
    """
    
    @requires_auth
    def hpost(self, user, domain_name):
        '''
        Create Domain
        '''
        return ApiResponse(code.SUCCESS, [])
    
        
    #def hget(self, *p):
    #    logging.info("Domain, GET: %s" % (p, ))


class ApiDomainUserCollection(BaseApi):
    
    def hget(self, *p):
        
        logging.info("Domain, GET: %s" % (p, ))



app = webapp2.WSGIApplication([
                                ('/_api/domain',           ApiDomainCollection)
                               ,('/_api/domain/(.*)',      ApiDomain)
                               ,('/_api/domain/(.*)/user', ApiDomainUserCollection)
                               ])
