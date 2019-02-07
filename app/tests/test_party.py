from .skeleton_test import Skeleton
from app.version1.routes import parties

class TestParty(Skeleton):

    def setUp(self):
        super().setUp()
        
        self.party = {
            "name": "Kanu",
            "hqAddress": "Eldoret",
            "logo_url":"url"
        }
    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        parties.clear()

    def test_create_party(self):
        res = self.client.post('/api/version1/parties', json = self.party)
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

    def test_get_party(self):
        self.client.post('/api/version1/parties', json=self.party)

        res = self.client.get('/api/version1/parties/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was successful')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_edit_party(self):
        self.client.post('/api/version1/parties', json=self.party)

        res = self.client.patch('/api/version1/parties/1/Kanu')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Kanu updated successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(data['data'][0]['name'], 'Kanu')
        self.assertEqual(res.status_code, 200)

    def test_delete_party(self):
        self.client.post('/api/version1/parties', json=self.party)

        res = self.client.delete('/api/version1/parties/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Kanu deleted successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)