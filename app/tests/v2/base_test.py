from app import create_app
import unittest
from app.v2.db.database_config import Database
from app.v2.models.parties_model import Party
from app.v2.models.offices_model import Office


class Base(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.item_list = []

    def tearDown(self):
        self.app = None
        self.item_list.clear()
        Office.offices.clear()
        Party.parties.clear()
