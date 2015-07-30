/*
 * Handles the 'Domains' section
 * 
 * @author: jldupont
 */
(function(document){
	'use strict';

	
	var setup = function(){
		
	  var mbus = document.querySelector("#mbus");

	  mbus.subscribe('X-user', function(data){
		  console.log("section_domains: X-user: ", data);
	  });
		
	};//setup
	
	
	app.addEventListener('dom-change', function() {
		setup();
	});
	
	
})(document);