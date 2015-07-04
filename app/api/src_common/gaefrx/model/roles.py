'''
Created on Jul 4, 2015

@author: jldupont
'''

from pyrbac import Role, define_permissions
from pyrbac import Create, Read, Update, Delete, List

from domain import Domain

class Manager(Role):
    '''
    The Manager role conveys permissions at a specific domain level
    '''
    permissions = define_permissions([
                                      (Domain, Read)
                                      ,(Domain, Update)
                                      ])
    