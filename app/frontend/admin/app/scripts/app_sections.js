/*
 * @author: jldupont
 * 
 * Dependencies:  
 * - underscore.js
 * - api
 * 
 */

(function(document) {
  'use strict';

  var current_user = null;
  
  var sections = [];
 
  
  var process_sections = function(){
	  
	  sections = document.querySelectorAll("[data-required-permission]");
	  
	  _.each(sections, function(section){
		  
		  var required_permission = section.getAttribute('data-required-permission');
		  var result = rbac.ensure(current_user, required_permission);
		  
		  //console.log("Section: ", section);
		  
		  if (api.get_option('debug'))
			  console.log("permission: ", required_permission, "  result: ", result);
		  //console.log("result: ", result);
		  
		  show_hide_section(section, result);
	  });
	  
	  
  };
  
  
  var show_hide_section = function(section, show_or_hide){
	  
	  if (show_or_hide)
		  section.removeAttribute('hidden');
	  else
		  section.setAttribute('hidden', true);
		  
  };
  
  
  var setup = function(){
	  
	  mbus.subscribe('X-user', function(data) {

		  current_user = data;
		  process_sections();
	  });
	  
	  mbus.subscribe('X-user_signout', function(_) {
		  console.log("User Signout event!");
		  
		  current_user = {};
		  process_sections();
	  });
	  
  };
  
  
  // Listen for template bound event to know when bindings
  // have resolved and content has been stamped to the page
  app.addEventListener('dom-change', function() {
    setup();
  });

})(document);
