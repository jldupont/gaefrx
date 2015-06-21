
import os, logging #@UnusedImport
import webapp2


class RouterApp(webapp2.RequestHandler):
    
    def get(self, *p, **k):
        '''
        '''
        logging.info("API GET: %s %s" % (p, k))


app = webapp2.WSGIApplication([
                               ('/(.*)',        RouterApp)
                               ], debug=True)
