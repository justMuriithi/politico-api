import unittest
import os
import json
from app import create_app


class PartyTestCase(unittest.TestCase):
    """This class represents the party test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.party = {'name': 'Kenya Parties'}


    def test_party_creation(self):
        """Test API can create a party (POST request)"""
        res = self.client().post('/party/', data=self.party)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Kanu', str(res.data))

    def test_api_can_get_all_parties(self):
        """Test API can get a party (GET request)."""
        res = self.client().post('/party/', data=self.party)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/party/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Kanu', str(res.data))

    def test_api_can_get_parties_by_id(self):
        """Test API can get a single party by using it's id."""
        rv = self.client().post('/party/', data=self.party)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/party/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Kanu', str(result.data))

    def test_parties_can_be_edited(self):
        """Test API can edit an existing party. (PUT request)"""
        rv = self.client().post(
            '/party/',
            data={'name': 'Republican'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/party/1',
            data={
                "name": "Democrat"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/party/1')
        self.assertIn('Demo', str(results.data))

    def test_parties_deletion(self):
        """Test API can delete an existing party. (DELETE request)."""
        rv = self.client().post(
            '/party/',
            data={'name': 'Republican'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/party/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/party/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
       


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()