/**
 * Session Management
 * 
 * 
 * @author: jldupont
 * 
 * Dependencies:
 */

(function(document) {
  'use strict';

  var mbus = null;
  
  var current_signin = null;
  var current_user = null;
  var current_user_id = null;
  var current_user_profile = null;
  
 
  var setup = function(){
	  
	  var mbus = document.querySelector("#mbus");
	
	  mbus.addEventListener('X-user_signin', function(event){
		  
		  var data = event.detail;
		  
		  current_signin = data;
		  
		  api.set_signin( current_signin );
		  
		  api.session_create({
			  cb_success: function(_, status, response_object) {
				  console.log("Session Create Success: ", response_object);
				  
				  current_user = response_object;
				  
				  mbus.async(function(){
					  mbus.fire('X-user', current_user);
				  });
				  
			  },
			  cb_error: function(_, status, response) {
				  console.log("Session Create Error: ", response);
			  }
		  });
		  
	  });

	  mbus.addEventListener('X-user_signout', function(data){
		  
		  var clear = function(){
			  api.set_signin( {} );
			  current_user = {};
			  current_signin = {};
		  };
		  
		  api.session_terminate({
			  cb_success: function(_, status, response) {
				  console.log("Session Terminate Success: ", response);
				  clear();
			  },
			  cb_error: function(_, status, response) {
				  console.log("Session Terminate Error: ", response);
				  clear();
			  }
		  });
		  
	  });
	  
	  
  };
  
  
  // Listen for template bound event to know when bindings
  // have resolved and content has been stamped to the page
  app.addEventListener('dom-change', function() {
    setup();
  });

})(document);
