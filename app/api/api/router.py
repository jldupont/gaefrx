'''
    API router
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

import setup #@UnusedImport

from gaefrx.api import BaseApi


class RouterApp(BaseApi):
    
    def get(self, *p):
        '''
        '''
        
        logging.info("API GET: %s" % (p, ))


app = webapp2.WSGIApplication([
                               ('/(.*)',        RouterApp)
                               ], debug=True)
