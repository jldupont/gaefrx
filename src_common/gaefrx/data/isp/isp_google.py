'''
Created on Jul 9, 2015

@author: jldupont
'''
import os, logging

from oauth2client import client#, crypt

from isp_base import BaseIsp

try:
    CLIENT_ID = os.environ['GOOGLE_SIGNIN_CLIENT_ID']
except:
    logging.error("Environ: %s" % repr(os.environ))
    raise Exception("Is secrets.yaml setup correctly ?")


class IspGoogle(BaseIsp):
    
    def verify(self, token):
        
        idinfo = client.verify_id_token(token, CLIENT_ID)
        
        logging.log("idinfo: %s" % repr(idinfo))