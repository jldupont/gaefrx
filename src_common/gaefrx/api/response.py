'''
The API response class

Created on Jun 26, 2015

@author: jldupont
'''

import code


class ApiResponse():
    """
    For constructing a reponse to an API request
    """
    
    def __init__(self, status_code, data={}, cursor = None):
        
        assert (status_code in code.all_codes), "Expecting a valid code, got '%s'" % repr(status_code)
        
        self.code = status_code
        self.data = data
        self.cursor = cursor
        