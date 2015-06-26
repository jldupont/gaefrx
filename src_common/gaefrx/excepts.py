'''
The exceptions

Created on Jun 26, 2015

@author: jldupont
'''

class ApiError(Exception):
    """
    Base for the whole API
    """


class MaybeRecoverableError(Exception):
    """
    Maybe be used as retry trigger
    """

class UnrecoverableError(Exception):
    """
    Denotes an unrecoverable error
    """


class ImplementationError(UnrecoverableError):
    """
    Base for all implementation errors
    
    I.e. can't recover because it is a design/implementation error
    """

class BadRequestError(ApiError):
    '''
    The API request contains errors (e.g. malformed fields)
    '''
    
class UnsupportedMethodError(ApiError):
    """
    The method is not supported
    """