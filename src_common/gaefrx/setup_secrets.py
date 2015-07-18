'''
Created on Jul 18, 2015

@author: jldupont
'''

import os
import yaml

dn = os.path.dirname

##
##  Update python path with 'src_common' directory
##
three_dirs_up = dn(dn(dn(__file__)))

secrets_yaml_path = os.path.join(three_dirs_up, '_config/secrets.yaml')

with open(secrets_yaml_path) as stream:
    secrets = yaml.load(stream)

os.environ.update(secrets['env_variables'])
