/**
 * API : session 
 * 
 * @author: jldupont
 * 
 * 
 **/

/*
 *  Create an authenticated session
 *  
 *  The user details should have been set prior
 *  
 *  @param context {
 *    cb_success [optional]
 *    cb_error   [optional]
 *  }
 */
api.session_create = function(context) {
	
	api.request({
		path: 'session',
		verb: 'post',
		cb_success: context && context.cb_success,
		cb_error:   context && context.cb_error
	});
};

/*
 *  Terminate an authenticated session
 *  
 *  @param context {
 *    cb_success [optional]
 *    cb_error   [optional]
 *  }
 */
api.session_terminate = function(){

	api.request({
		path: 'session',
		verb: 'delete',
		cb_success: context && context.cb_success,
		cb_error:   context && context.cb_error
	});	
};
