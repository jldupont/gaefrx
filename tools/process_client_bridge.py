#!/usr/bin/python
"""
@author:  Jean-Lou Dupont - 24 June 2015
"""

import os
import sys

dn = os.path.dirname
two_dirs_up = dn(dn(__file__))

#
# Path to AppEngine's SDK
#
gae_path = os.path.expandvars("$GOOGLE_APPENGINE")
sys.path.insert(0, gae_path)

#
# Paths to the projects package directories
#
sys.path.insert(0, os.path.join(two_dirs_up,'src_common'))
sys.path.insert(0, os.path.join(two_dirs_up,'src_ext'))


from pyrbac import export

import gaefrx.model.roles #@UnusedImport

def rbac_json_repr():
    '''
    Returns a JSON string representation of the defined Roles
    '''
    return export()

print rbac_json_repr()