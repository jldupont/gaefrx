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

api._request_base = "/_api/";
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


api._build_query_string = function(params) {
	
    var queryParts = [];
    var param;
    var value;

    for (param in params) {
    	
      value = params[param];
      param = window.encodeURIComponent(param);

      if (value !== null) {
        param += '=' + window.encodeURIComponent(value);
      }

      queryParts.push(param);
    }

    return queryParts.join('&');
};


/*
 * The intermediate request layer
 * 
 * @param context: object:
 * 				verb: string
 * 				path: string
 * 				query_parameters: object
 * 				headers: object
 * 				json_body : optional when 'null'
 * 				cb_success : callback used when request is successful
 * 				cb_error   : callback used when request is unsuccessful
 */
api._request = function(context){
	
	var qs = api._build_query_string(context.query_parameters || {});
	var url = api._request_base + context.path;
	
	if (qs!="")
		url += "?"+qs;
	
	context.url = url;
	
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

      if (context.headers) {
    	  
          Object.keys(context.headers).forEach(function (requestHeader) {
            xhr.setRequestHeader(
              requestHeader,
              context.headers[requestHeader]
            );
          });
      };
      
      xhr.open(
        context.verb || 'GET',
        context.url,
        context.async || true
      );	
	
      xhr.send(context.body);
};