'''
Created on Jun 26, 2015

@author: jldupont
'''
import logging  #@UnusedImport
import json
import webapp2

from pyrbac import ensure, PermissionError

from gaefrx.api.response import ApiResponse
import gaefrx.api.code as code 

from gaefrx.excepts import ImplementationError, BadRequestError, UnsupportedMethodError
from gaefrx.excepts import UnauthorizedError, NotFoundError, RemoteServiceError, DatastoreError
from gaefrx.excepts import ExistsError

from gaefrx.data.user import ensure_authentication


class accept_parameters(object):
    '''
    Decorator - helper for url parameters
    '''
    def __init__(self, list_parameter_name):
        self.params = list_parameter_name
        
    def __call__(self, fnc):
        self.fnc = fnc
        return self._inject_params

    def _inject_params(self, this, *p):
        '''
        Extract the sought parameters
         and inject them in the keyword parameters
         of the target method 
        '''
        values = { key: this.request.get(key, None) for key in self.params}
        return self.fnc(this, *p, **values)
        

class requires_permission(object):
    '''
    Decorator - check permission
    
    @raise PermissionError
    '''
    
    _DEBUG = False
    
    def __init__(self, permission):
        self.permission = permission
        
    def __call__(self, fnc):
        self.fnc = fnc
        return self._check_permission

    def _check_permission(self, this, user, *p):
        '''
        Expecting 'user' as first parameter
        @raise PermissionError
        '''
        if not self._DEBUG:
            ensure(user, self.permission)
            
        return self.fnc(this, user, *p)


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
        
        result, user = ensure_authentication(ctx) 
        
        if not result:
            raise UnauthorizedError() 
        
        return method(this, user, *pargs)

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
        if self.nheaders is None:
            self._normalize_headers()
        
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
        
        try:
            
            maybe_response  = self._dispatcher(verb, *p)
            
            if not isinstance(maybe_response, ApiResponse):
                raise ImplementationError('Expecting ApiResponse instance for %s:%s' % (self.__class__.__name__, verb))

            self._generate_response(maybe_response)

        except (PermissionError, UnauthorizedError),e:
            self._generate_response_error(code.FORBIDDEN, e)

        except (RemoteServiceError, DatastoreError), e:
            self._generate_response_error(code.SERVICE_UNAVAILABLE, e)

        except (NotFoundError,), e:
            self._generate_response_error(code.NOT_FOUND_ERROR, e)
        
        except (ImplementationError,), e:
            self._generate_response_error(code.SERVER_ERROR, e)
            
        except (BadRequestError, ExistsError), e:
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
            
            data = response_object.data
            
            try:
                json_repr = json.dumps( data.to_json() )
            except:
                json_repr = json.dumps( data )
            
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
    
    def hoptions(self, *_):
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
