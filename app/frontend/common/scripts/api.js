/**
 * Javascript API to gaefrx 
 * 
 * @author: jldupont
 * 
 **/

api = {};

// -------------------------------------------------------- PUBLIC parameters

api.debug = false;


//-------------------------------------------------------- PRIVATE parameters

api._request_base = "/api/";
api._current_user = {};
api._options = {};

//-------------------------------------------------------- PUBLIC functions

/*
 *  Setting the User related parameters
 *  
 *  This can be done one time at the beginning of a session
 *  
 *  @param user_details : an object containing the details
 */
api.set_user = function(user_details){
  api._current_user = user_details;	
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

//-------------------------------------------------------- PRIVATE functions

/*
 * The intermediate request layer
 * 
 * @param verb
 * @param path
 * @param query_parameters
 * @param headers
 * @param body : optional when 'null'
 * @param cb_success : callback used when request is successful
 * @param cb_error   : callback used when request is unsuccessful
 */
api._request = function(verb, path, query_parameters, headers, body, cb_success, cb_error){
	
};

/*
 * The lowest layer
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
        	if ((xhr.status>=200) && (xhr.status<300))
        		do_callback(context.cb_success, xhr.status, xhr.responseText);
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
	
      xhr.send(context.body);
};