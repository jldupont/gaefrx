'''
    API - Domain resource
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

import setup #@UnusedImport

from pyrbac import Permission, Create, List, Read, Delete

from gaefrx.excepts import InvalidParameterValueError, ExistsError, NotFoundError

from gaefrx.api.base import BaseApi, requires_auth, requires_permission, accept_parameters
from gaefrx.api.response import ApiResponse
import gaefrx.api.code as code

import gaefrx.data.domain as ddomain

class ApiDomainCollection(BaseApi):

    @requires_auth
    @requires_permission(Permission(ddomain.Domain, List))    
    @accept_parameters(['cursor', 'count'])
    def hget(self, _user, **params):
        '''
        Retrieve a list of domains
        '''
        
        domains, cursor, more = ddomain.read_page(**params)
        
        domains_repr = ddomain.export_domain(domains)
        
        return ApiResponse(code.SUCCESS, {
                                          'domains': domains_repr
                                          ,'cursor': cursor
                                          ,'more':   more
                                          })



class ApiDomain(BaseApi):
    """
    The API for the resource 'Domain'
    """
    
    @requires_auth
    @requires_permission(Permission(ddomain.Domain, Read))
    def hget(self, user, name):
        '''
        Get Domain
        
        Checks for duplicates
        
        @raise InvalidParameterValueError
        @raise DatastoreError
        @raise ExistsError 
        '''
        if not isinstance(name, basestring):
            raise InvalidParameterValueError('name')
            
        name = name.lower()
            
        maybe_domain = ddomain.get_by_name(name)
        if maybe_domain is None:
            raise NotFoundError()
        
        return ApiResponse(code.SUCCESS, maybe_domain)
    
    
    @requires_auth
    @requires_permission(Permission(ddomain.Domain, Create))
    def hpost(self, user, name):
        '''
        Create Domain
        
        Checks for duplicates
        
        @raise InvalidParameterValueError
        @raise DatastoreError
        @raise ExistsError 
        '''
        if not isinstance(name, basestring):
            raise InvalidParameterValueError('name')
            
        name = name.lower()
            
        maybe_domain = ddomain.get_by_name(name)
        if maybe_domain is not None:
            raise ExistsError()
        
        d = ddomain.create(name)
        
        return ApiResponse(code.SUCCESS, d)
    
    @requires_auth
    @requires_permission(Permission(ddomain.Domain, Delete))
    def hdelete(self, user, name):
        '''
        Create Domain
        
        Checks for duplicates
        
        @raise InvalidParameterValueError
        @raise DatastoreError
        @raise ExistsError 
        '''
        if not isinstance(name, basestring):
            raise InvalidParameterValueError('name')
            
        name = name.lower()
            
        maybe_domain = ddomain.get_by_name(name)
        if maybe_domain is None:
            raise NotFoundError()
    
        
        ddomain.delete(maybe_domain)
        
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
