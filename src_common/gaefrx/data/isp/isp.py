'''
Identity Service Provider

Created on Jul 9, 2015

@author: jldupont
'''

from gaefrx.excepts import NotFoundError

from isp_base import MetaIsp



def lookup_provider(name):
    '''
    @param name: the isp name
    @return BaseIsp subclass
    @raise  NotFoundError
    '''
    assert isinstance(name, basestring), 'expected string, got: %s' % repr(name)
    try:
        return MetaIsp.isps[name]
    except:
        raise NotFoundError('realm: %s' % repr(name))
    