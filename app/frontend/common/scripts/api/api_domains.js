/**
 * API : domains 
 * 
 * @author: jldupont
 * 
 * 
 **/

/*
 *  Create a Domain
 *  
 *  @param context {
 *    name
 *    cb_success [optional]
 *    cb_error   [optional]
 *  }
 */
api.domain_create = function(context) {
	
	api.request({
		path: 'domain/'+context.name,
		verb: 'post',
		cb_success: context && context.cb_success,
		cb_error:   context && context.cb_error
	});
};

/*
 *  List Domains
 *  
 *  @param context {
 *    cursor
 *    cb_success [optional]
 *    cb_error   [optional]
 *  }
 */
api.domain_list = function(context) {
	
	var params = _.clone(context);
	
	delete params.cb_success;
	delete params.cb_error;
	delete params.cb_exception;
	
	api.request({
		path: 'domain'+uri.build_query_string(params),
		verb: 'get',
		cb_success: context && context.cb_success,
		cb_error:   context && context.cb_error
	});
};
