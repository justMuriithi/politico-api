from app import create_app
import unittest

class Skeleton(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.item_list = []


    def tearDown(self):
        self.app = None
        self.item_list.clear()
