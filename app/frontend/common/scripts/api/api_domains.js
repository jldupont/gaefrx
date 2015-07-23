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
 *    cb_success [optional]
 *    cb_error   [optional]
 *  }
 */
api.domain_create = function(context) {
	
	api.request({
		path: 'domain/'+context.domain_name,
		verb: 'post',
		cb_success: context && context.cb_success,
		cb_error:   context && context.cb_error
	});
};
