'''
Created on Jul 9, 2015

@author: jldupont
'''
import os, logging

from oauth2client import client, crypt

from gaefrx.excepts import NotFoundError, RemoteServiceError
from isp_base import BaseIsp

try:
    CLIENT_ID = os.environ['GOOGLE_SIGNIN_CLIENT_ID']
except:
    raise Exception("Is secrets.yaml setup correctly ?")


class IspGoogle(BaseIsp):
    
    @classmethod
    def verify(cls, token):
        '''
        @return user info dict { domain, name_last, name_first, user_id }
        @raise NotFoundError
        @raise RemoteServiceError
        '''
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)
            
            if idinfo['aud'] != CLIENT_ID:
                raise NotFoundError('wrong issuer')
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise NotFoundError('wrong issuer')
            
        except crypt.AppIdentityError:
            raise NotFoundError()
        
        except Exception, e:
            logging.debug("IspGoogle: %s" % repr(e))
            raise RemoteServiceError()
            
        return {
                 'email':       idinfo['email']
                 ,'domain':     idinfo.get('hd', None)
                 ,'name_last':  idinfo['family_name']
                 ,'name_first': idinfo['given_name']
                 ,'user_id':    idinfo['sub']
                 ,'token':      token
                } 