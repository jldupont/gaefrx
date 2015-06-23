'''
    API router
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

import setup #@UnusedImport


class RouterApp(webapp2.RequestHandler):
    
    def get(self, *p):
        '''
        '''
        
        logging.info("API GET: %s" % (p, ))


app = webapp2.WSGIApplication([
                               ('/(.*)',        RouterApp)
                               ], debug=True)
