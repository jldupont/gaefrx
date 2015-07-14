'''
Created on Jul 9, 2015

@author: jldupont
'''
import os, logging

from oauth2client import client#, crypt

from gaefrx.excepts import NotFoundError
from isp_base import BaseIsp

try:
    CLIENT_ID = os.environ['GOOGLE_SIGNIN_CLIENT_ID']
except:
    raise Exception("Is secrets.yaml setup correctly ?")


class IspGoogle(BaseIsp):
    
    @classmethod
    def verify(cls, token):
        '''
        @return user info dict
        @raise NotFoundError
        
        @todo: cannot trap this error  
        @raise RemoteServiceError
        '''
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)
            
            if idinfo['aud'] != CLIENT_ID:
                raise NotFoundError('wrong issuer')
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise NotFoundError('wrong issuer')
            
        except:
            raise NotFoundError()
        
        logging.info("idinfo: %s" % repr(idinfo))