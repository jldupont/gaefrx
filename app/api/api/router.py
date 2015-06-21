'''
    API router
    
    @author: Jean-Lou Dupont
'''
import os, sys, logging #@UnusedImport
import webapp2

dn = os.path.dirname

##
##  Update python path with 'src_common' directory
##
two_dirs_up = dn(dn(__file__))
sys.path.append(os.path.join(two_dirs_up, 'src_common'))


class RouterApp(webapp2.RequestHandler):
    
    def get(self, *p):
        '''
        '''
        logging.info("API GET: %s" % (p, ))


app = webapp2.WSGIApplication([
                               ('/(.*)',        RouterApp)
                               ], debug=True)
