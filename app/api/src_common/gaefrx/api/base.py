'''
Created on Jun 26, 2015

@author: jldupont
'''
import json
import webapp2

from gaefrx.excepts import BadRequestError

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
    
    def __getattr__(self, verb):
        '''
        '''
        _verb = verb.lower()
        
        if _verb in self.HTTP_VERBS:
            
            def _(*p):
                return self._handler(verb, *p)
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
            ##
            ## resp: the response object
            ##
            ## created: if a resource was created as a result of this request
            ##
            ## more: if there are more data available through a subsequent request using the cursor
            ##
            ## cursor: the cursor to use for a subsequent request
            ##         This parameter should already be 'urlsafe'
            ##
            resp = {}
            code = 200
            
            raw_resp, created, more, cursor = self._dispatcher(verb, *p)
            
            if created:
                code = 201
            
            if more:
                resp['cursor'] = cursor
            
            if raw_resp is not None:
                resp['data'] = raw_resp
            
            self._generate_response(code, resp)
            
        except (BadRequestError,), e:
            self._generate_response_error(405, e)


    def _generate_response_error(self, status_code, exception):
        '''
        Generates an error response back
        '''
        self.response.headers['Content-Type'] = "application/json"

        response_object = {
                            'eclass': exception.__class__.__name__
                           ,'emsg':   exception.message
                           }
        
        self._generate_response(status_code, response_object)
    

    def _generate_response(self, status_code, response_object = None):
        '''
        Generates the response back
        '''
        if response_object is not None:
            
            ##
            ## We expect a non-empty dict
            ##
            if len(response_object) > 0:
                self.response.headers['Content-Type'] = "application/json"
                json_repr = json.dumps(response_object)
                self.response.out.write(json_repr)
            
        self.response.set_status(status_code)




class BaseApi(webapp2.RequestHandler):
    '''
    The base class which should be used by API handlers
    '''
    
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
        return handler(*p)
    
    def hget(self, *p):
        """
        The default 'GET' verb
        """
        ######  resp, created, more,  cursor
        return (None, False,   False, None)

    def hpost(self, *p):
        """
        The default 'POST' verb
        """
        ######  resp, created, more,  cursor
        return (None, False,   False, None)

    def hput(self, *p):
        """
        The default 'PUT' verb
        """
        ######  resp, created, more,  cursor
        return (None, False,   False, None)

    def hdelete(self, *p):
        """
        The default 'DELETE' verb
        """
        ######  resp, created, more,  cursor
        return (None, False,   False, None)

