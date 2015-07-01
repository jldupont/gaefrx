/*
 * @author: jldupont
 */

(function(document) {
  'use strict';

  var mbus = null;
  var current_user = null;
  
 
  var setup = function(){
	  
	  var mbus = document.querySelector("#mbus");
	  
	  mbus.addEventListener('X-user_signin', function(details) {
		  console.log("User Signin event!");
	  });
	  
	  mbus.addEventListener('X-user_signout', function(details) {
		  console.log("User Signout event!");
	  });
	  
  };
  
  
  // Listen for template bound event to know when bindings
  // have resolved and content has been stamped to the page
  app.addEventListener('dom-change', function() {
    setup();
  });

})(document);
