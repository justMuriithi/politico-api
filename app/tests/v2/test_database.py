import unittest
from app.v2.db.database_config import Database
from app.v2.models.user_model import User


class TestDatabase(unittest.TestCase):
    """ Test database """

    def setUp(self):
        """ set up tests """

        self.db = Database('development')
        self.db.create_db()
        self.db.create_super_user()

    def test_connect_db(self):
        """ Test whether connection is established """

        db = Database('development')
        self.assertTrue(db.init_connection())

    def test_connect_test_db(self):
        """ Test whether connection is established on test db """

        db = Database('testing')
        self.assertTrue(db.init_connection())

    def test_super_user_created(self):
        """ Tests whether the super user was created """

        admin = User().find_by('email', 'antoineshephmaina@gmail.com')
        self.assertTrue(admin)
        self.assertEqual(admin['firstname'], 'Tony')
