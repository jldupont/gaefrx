'''
Created on Jun 24, 2015

@author: jldupont
'''
import unittest

from google.appengine.ext import ndb

from pyrbac import Admin, Guest
from gaefrx.model.custom import RolesProperty


class TestEntity(ndb.Model):
    
    roles = RolesProperty()


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testRolesProperty(self):
        
        roles = [Admin, Guest]
        
        te = TestEntity()
        te.roles = roles
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()