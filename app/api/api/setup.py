'''
Created on Jun 23, 2015
@author: jldupont
'''
import os, sys

import yaml

dn = os.path.dirname

##
##  Update python path with 'src_common' directory
##
two_dirs_up = dn(dn(__file__))
sys.path.append(os.path.join(two_dirs_up, 'src_common'))
sys.path.append(os.path.join(two_dirs_up, 'src_ext'))

secrets_yaml_path = os.path.join(two_dirs_up, '_config/secrets.yaml')

with open(secrets_yaml_path) as stream:
    secrets = yaml.load(stream)

os.environ.update(secrets['env_variables'])
