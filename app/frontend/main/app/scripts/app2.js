/*
 *  Tests 
 *  
 *  @author: jldupont
 */
(function(document) {
  'use strict';

  

  var setup=function(){

	  var greet = document.querySelector('#thegreet');
	  
	  greet.addEventListener("was-changed", function(){
		  console.log("My-Greeting was changed!");
	  });
	  
  };
  
  var app = document.querySelector('#app');
  app.addEventListener('dom-change', function() {
	    setup();
  });
  

})(document);
