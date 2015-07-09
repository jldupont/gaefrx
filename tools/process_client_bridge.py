#!/usr/bin/python
"""
@author:  Jean-Lou Dupont - 24 June 2015
"""

import os
import sys

print "Generating client_bridge.js ..."
#
# Configuration
#
where_to_create_files = [
                          'app/frontend/admin/app/scripts/client_bridge.js'
                         ,'app/frontend/main/app/scripts/client_bridge.js'
                         ]


## --------------------------------------------------------------
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


template = """// This file is auto-generated
roles = %s;
"""

script_file_contents = template % (export())

for file_to_create_or_update in where_to_create_files:
    
    fpath = os.path.join(two_dirs_up, file_to_create_or_update)
    hfile = open(fpath, 'w')
    hfile.write( script_file_contents )
    hfile.close()
    
print "Success !"