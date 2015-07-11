'''
Created on Jun 26, 2015

@author: jldupont
'''
#import logging
import json
import webapp2

from gaefrx.api.response import ApiResponse
from gaefrx.api import code
from gaefrx.excepts import ImplementationError, BadRequestError, UnsupportedMethodError
from gaefrx.excepts import UnauthorizedError

from gaefrx.data.user import ensure_authentication



def requires_auth(method):
    '''
    Decorator - check authentication
    
    Should only be used in a _RootApi subclass
    
    @raise UnauthorizedError
    @raise BadRequestError
    @raise NotFoundError
    '''
    def _(this, *pargs):
        
        ctx = this.get_context()
        if not ensure_authentication(ctx):
            raise UnauthorizedError() 
        
        return method(this, *pargs)

    return _




class _RootApi(webapp2.RequestHandler):
    '''
    The base class which should be used by API handlers
    '''
    
    HTTP_VERBS = ['get', 'post', 'put', 'delete', 'head', 'options']
    
    
    def _normalize_headers(self):
        """
        All Headers and Cookies keys normalized to lowercase
        """
        self.ncookies=dict((k.lower(), v) for k, v in self.request.cookies.iteritems())
        self.nheaders=dict((k.lower(), v) for k, v in self.request.headers.iteritems())
    
    def get_context(self):
        '''
        Return the request context
         i.e. realm, user name, email and token
         
        @return {...}
        '''
        return {
                 'name':  self.nheaders.get('x-name',  None)
                ,'email': self.nheaders.get('from',    None)
                ,'token': self.nheaders.get('x-token', None)
                ,'realm': self.nheaders.get('x-realm', None)
                }
    
    def __getattr__(self, verb):
        
        _verb = verb.lower()
        
        if _verb in self.HTTP_VERBS:
            
            def _(*p):
                return self._handler(_verb, *p)
            return _
        
        ## Must respond with the default
        ##
        return self.__dict__.get(verb, None)
      
    def _handler(self, verb, *p):
        '''
        Attempts to dispatch request
        
        Dispatches to the verb handler
         using the pattern 'h$verb'        
        '''
        self._normalize_headers()
        
        try:
            
            maybe_response  = self._dispatcher(verb, *p)
            
            if not isinstance(maybe_response, ApiResponse):
                raise ImplementationError('Expecting ApiResponse instance for %s:%s' % (self.__class__.__name__, verb))

            self._generate_response(maybe_response)
        
        except (ImplementationError,), e:
            self._generate_response_error(code.SERVER_ERROR, e)
            
        except (BadRequestError, ), e:
            self._generate_response_error(code.BAD_REQUEST, e)

        except (UnsupportedMethodError, ), e:
            self._generate_response_error(code.METHOD_NOT_ALLOWED, e)


    def _generate_response_error(self, status_code, exception):
        '''
        Generates an error response back
        '''
        self.response.headers['Content-Type'] = "application/json"

        response_body  = {
                            'eclass': exception.__class__.__name__
                           ,'emsg':   exception.message
                           }
        
        response_object = ApiResponse(status_code, data = response_body)
        
        self._generate_response(response_object)
    

    def _generate_response(self, response_object):
        '''
        Generates the response back
        '''
        assert isinstance(response_object, ApiResponse), "Expecting ApiResponse, got %s" % repr(response_object)
        
        ##
        ## We expect a non-empty dict
        ##
        if response_object.data is not None:
            self.response.headers['Content-Type'] = "application/json"
            json_repr = json.dumps(response_object.data)
            self.response.out.write(json_repr)
            
        if self.CORS_ENABLED:
            self.response.headers["Access-Control-Allow-Origin"] = "*"
            self.response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, HEAD, DELETE, OPTIONS"
            self.response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, From, X-token, X-realm'
            
        self.response.set_status(response_object.code)




class BaseApi(_RootApi):
    '''
    The base class which should be used by API handlers
    '''
    
    CORS_ENABLED = True
    
    def setup(self):
        '''
        This method can be used to process the request
         before dispatching to the handler.
         
        This can be useful for constructing a User instance
         with the request headers, as example.
        '''
    
    def _dispatcher(self, verb, *p):
        
        handler=getattr(self, "h%s" % verb)
        if handler is None:
            raise BadRequestError("unsupported method: %s" % verb)
        
        self.setup()
        response = handler(*p)
        
        ##
        ## Help for the usual case
        ##
        if response is None:
            return ApiResponse(code.SUCCESS)
        
        return response
    
    def hoptions(self):
        '''
        The CORS pre-flight verb
        '''
        
        if self.CORS_ENABLED:
            return ApiResponse(code.SUCCESS)
        
        return ApiResponse(code.METHOD_NOT_ALLOWED)

    
    def hget(self, *p):
        """
        The default 'GET' verb
        """
        raise UnsupportedMethodError('get')

    def hpost(self, *p):
        """
        The default 'POST' verb
        """
        raise UnsupportedMethodError('post')
    
    def hput(self, *p):
        """
        The default 'PUT' verb
        """
        raise UnsupportedMethodError('put')
    
    def hdelete(self, *p):
        """
        The default 'DELETE' verb
        """
        raise UnsupportedMethodError('delete')

