/**
 * Session Management
 * 
 * 
 * @author: jldupont
 */

(function(document) {
  'use strict';

  var mbus = null;
  var current_user = null;
  var current_user_id = null;
  var current_user_profile = null;
  
 
  var setup = function(){
	  
	  var mbus = document.querySelector("#mbus");
	
	  mbus.addEventListener('X-user_signin', function(){
		  
	  });

	  mbus.addEventListener('X-user_signout', function(){
		  
	  });
	  
	  
  };
  
  
  // Listen for template bound event to know when bindings
  // have resolved and content has been stamped to the page
  app.addEventListener('dom-change', function() {
    setup();
  });

})(document);
