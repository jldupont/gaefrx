/**
 * Javascript API to gaefrx 
 * 
 * @author: jldupont
 * 
 * @dependency: jldupont/js-uri-toolkit
 * 
 **/

api = {};

// -------------------------------------------------------- PUBLIC parameters


//-------------------------------------------------------- PRIVATE parameters

api._current_signin = {};
api._context = {};
api._options = {};

// we need to limit the damage that can be done through XSS
api._url_allowed_parameters = ['port', 'debug'];

//-------------------------------------------------------- PUBLIC functions

/*
 *  This method should be called upon initial application loading
 *  
 *  The initialization consists in preparing the API request context :
 *  - Extract relevant parameters from the application URL
 *    - api_port
 *    - api_debug
 *  
 */
api.init = function(){
	
	var initial_url = window.location.href;
	api._context = uri.parse( initial_url );
	
	// extract the parameters relevant to this module
	_.mapObject(api._context.query, function(value, key){
		if (key.indexOf("api")==0) {
			var param_name = key.substr("api_".length);
			
			if (_.indexOf(api._url_allowed_parameters, param_name)!=-1)
				api._options[ param_name ] = value;
		}
			
	});
	
	// do we have a port specified for the server API ?
	api._context.port = api._options.port || api._context.port;
	
	api._context.base = "_api/";
};

/*
 *  Return scheme://host[:port]/
 */
api.get_host_and_port = function() {
	return uri.build_host(api._context);
};

/*
 *  Setting the Sign-In related parameters
 *  
 *  This can be done one time at the beginning of a session
 *  
 *  @param signin_details : an object containing the details
 *    - realm
 *    - name
 *    - token
 *    - email
 */
api.set_signin = function(signin_details){
  api._current_signin = signin_details || {};	
};

/*
 *  Delete the current signin
 *  
 */
api.del_signin = function(){
  api._current_signin = {};	
};


/*
 *  Setting the default options
 *  
 *  Options supported:
 *  - cb_success : the callback to use when a request is successful
 *  - cb_error:    the callback to use when a request is unsuccessful
 */
api.set_options = function(options){
	api._options = options;
};

/*
 *  Get an option value
 */
api.get_option = function(option_name) {
	var value = api._options[option_name] || null;
	
	if (value=='true' || value=='false')
		return !!value;
	
	var maybe_int = parseInt(value);
	if (maybe_int != NaN)
		return maybe_int;
	
	var maybe_float = parseFloat(value);
	if (maybe_float != NaN)
		return maybe_float;
	
	return value;
};


//-------------------------------------------------------- PRIVATE functions



/*
 * The intermediate request layer
 * 
 * @param context: object:
 * 				verb: string
 * 				path: string
 * 				query: object
 * 				headers: object
 * 				json_body : optional when 'null'
 * 				cb_success : callback used when request is successful
 * 				cb_error   : callback used when request is unsuccessful
 */
api.request = function(context){
	
	var rcontext = {};
	
	// we grab the basic URL components from the initial context
	rcontext.scheme = api._context.scheme; 
	rcontext.host   = api._context.host;
	rcontext.port   = api._context.port;
	
	// we inject the path and query string
	rcontext.path  = api._context.base + context.path;
	rcontext.query = context.query;
	
	context.url = uri.build(rcontext);
	
	context.headers = {
		'Content-Type': 'application/json',
		'From':         api._current_signin.email || null,
		'X-realm':      api._current_signin.realm || null,
		'X-token':      api._current_signin.token || null
	};
	
	return api._make_request(context);
};

/*
 * The lowest layer
 * 
 * @param context: object
 * 
 *   context.cb_success   [optional]
 *   context.cb_error     [optional]
 *   context.cb_exception [optional]
 *   context.headers
 *   context.url
 *   context.verb
 *   context.body
 *   
 */
api._make_request = function(context) {
	
	var xhr = new XMLHttpRequest();
	
	var do_callback = function(which_cb, status, response){
		if (which_cb) {
			try {
				which_cb(context, status, response);
			} catch(e) {
				if (context.cb_exception)
					try {
						context.cb_exception(context, status, response);
					} catch(e) {
						console.error("API: make request: ", e);
					}
			}
		}
			
	};
	
    xhr.addEventListener('readystatechange', function () {
    	
        if (xhr.readyState === 4) {
        	if ((xhr.status>=200) && (xhr.status<300)) {
        		
        		var response_object = JSON.parse(xhr.responseText);
        		do_callback(context.cb_success, xhr.status, response_object);
        	}
        		
        }

      });

      xhr.addEventListener('error', function (error) {
    	  do_callback(context.cb_error, xhr.status, xhr.responseText);
      });

      xhr.addEventListener('abort', function () {
    	  do_callback(context.cb_error, xhr.status, xhr.responseText);
      });

      xhr.open(
        context.verb || 'GET',
        context.url,
        context.async || true
      );	

      if (context.headers) {
    	  
          Object.keys(context.headers).forEach(function (requestHeader) {
            xhr.setRequestHeader(
              requestHeader,
              context.headers[requestHeader]
            );
          });
      };
            
      xhr.send(context.body);
};