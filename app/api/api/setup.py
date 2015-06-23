'''
Created on Jun 23, 2015
@author: jldupont
'''
import os, sys


dn = os.path.dirname

##
##  Update python path with 'src_common' directory
##
two_dirs_up = dn(dn(__file__))
sys.path.append(os.path.join(two_dirs_up, 'src_common'))
sys.path.append(os.path.join(two_dirs_up, 'src_ext'))
