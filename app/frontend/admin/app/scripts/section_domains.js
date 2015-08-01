/*
 * Handles the 'Domains' section
 * 
 * @author: jldupont
 */
(function(document){
	'use strict';

	
	var setup = function(){
		
	  mbus.subscribe('X-section', function(which_section){
		  
		  if (which_section=='domains')
			  console.log("section_domains selected");
	  });
		
	};//setup
	
	
	app.addEventListener('dom-change', function() {
		setup();
	});
	
	
})(document);