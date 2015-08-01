/*
 * Handles the 'Domains' section
 * 
 * @author: jldupont
 */
(function(document){
	'use strict';

	var page_domains = null;
	
	var setup = function(){
		
	  mbus.subscribe('X-section', function(which_section){
		  
		  if (which_section=='domains')
			  console.log("section_domains selected");
	  });
		
	};//setup
	
	mbus.subscribe("X-user", function(_details){
		
		var scheme_host_port = api.get_scheme_host_and_port();
		page_domains = document.body.querySelector("page-domains");
		
		var headers = api.get_headers();
		page_domains.init_api(scheme_host_port, headers);
	});
	
	  
	app.addEventListener('dom-change', function() {
		setup();
	});
	
	
})(document);