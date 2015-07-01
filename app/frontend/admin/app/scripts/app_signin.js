/*
 * @author: jldupont
 */

(function(document) {
  'use strict';

  var current_user = null;
  
  var setup = function(){
	  
	  var gsign = document.querySelector("#google_signin");
	  
	  gsign.addEventListener('google-signin-aware-success', function(result){
		  current_user = gapi.auth2.getAuthInstance().currentUser.get();
		  console.log("Google Sign-In Success!", current_user);
	  });
	  
	  gsign.addEventListener('google-signed-out', function(){
		  console.log("Google Sign-Out...");
		  current_user = null;
	  });
  };
  
  
  // Listen for template bound event to know when bindings
  // have resolved and content has been stamped to the page
  app.addEventListener('dom-change', function() {
    setup();
  });

})(document);
