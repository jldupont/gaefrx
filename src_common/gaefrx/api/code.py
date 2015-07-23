'''
Created on Jun 26, 2015

@author: jldupont
'''

##
## I put these outside of the ApiReponse class
##  definition in order to save typing when constructing
##  an instance of this class
##
SUCCESS = 200
CREATED = 201
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND_ERROR = 404
METHOD_NOT_ALLOWED = 405
SERVER_ERROR = 500
SERVICE_UNAVAILABLE = 503


all_codes = [ SUCCESS 
             ,CREATED
             ,BAD_REQUEST
             ,FORBIDDEN
             ,METHOD_NOT_ALLOWED
             ,SERVER_ERROR
             ,NOT_FOUND_ERROR 
             ]
