from .skeleton_test import Skeleton
from app.version1.routes import parties

class TestParty(Skeleton):

    def setUp(self):
        super().setUp()
        
        self.party = {
            "name": "Kanu",
            "hq_address": "Eldoret",
            "logo_url":"url"
        }
    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        parties.clear()

    def test_create_party(self):
        res = self.client.post('/api/version1/parties/', json = self.party)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Your political party was created successfully')
        self.assertEqual(res.status_code, 201)

    def test_get_parties(self):
        res = self.client.post('/api/version1/parties', json = self.party)
        res = self.client.post('/api/version1/parties', json = self.party)

        res = self.client.get('/api/version1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was successful')
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(res.status_code, 200)
