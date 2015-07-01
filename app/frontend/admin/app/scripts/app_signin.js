/*
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
	  var gsign = document.querySelector("#google_signin");
	  
	  gsign.addEventListener('google-signin-aware-success', function(result){
		  
		  current_user = gapi.auth2.getAuthInstance().currentUser.get();
		  current_user_id = current_user.getAuthResponse().id_token;
		  current_user_profile = current_user.getBasicProfile();
		  
		  //console.log("Google Sign-In Success!", current_user);
		  //console.log("Google User Id", current_user_id);
		  //console.log("Google User Profile", current_user.getBasicProfile());
		  
		  mbus.fire('X-user_signin', {
			  realm:   'google',
			  id:      current_user_id,
			  domain:  current_user.getHostedDomain(),
			  name:    current_user_profile.getName(),
			  email:   current_user_profile.getEmail()
		  });
		  
	  });
	  
	  gsign.addEventListener('google-signed-out', function(){
		  //console.log("Google Sign-Out...");
		  current_user = null;
		  
		  mbus.fire('X-user_signout', {});
	  });
  };
  
  
  // Listen for template bound event to know when bindings
  // have resolved and content has been stamped to the page
  app.addEventListener('dom-change', function() {
    setup();
  });

})(document);
