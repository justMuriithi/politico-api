from .base_test import Base
from app.version1.models.db import Database


class TestParty(Base):

    def setUp(self):
        super().setUp()

        self.parties = Database().get_table(Database.PARTIES)

        self.party = {
            "name": "Kanu",
            "hqAddress": "Eldoret"
        }
    # clear all lists after tests

    def tearDown(self):
        super().tearDown()

    def test_create_party(self):
        res = self.client.post('/api/version1/parties', json=self.party)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(
            data['message'], 'Your political party was created successfully')
        self.assertEqual(res.status_code, 201)

    def test_create_party_name_exists(self):
        res = self.client.post('/api/version1/parties', json=self.party)
        res = self.client.post('/api/version1/parties', json=self.party)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Party already exists')
        self.assertEqual(res.status_code, 400)

    def test_create_party_missing_fields(self):
        res = self.client.post('/api/version1/parties', json={
            "hqAddress": "Eldoret"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'name field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_party_no_data(self):
        res = self.client.post('/api/version1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_get_parties(self):
        res = self.client.post('/api/version1/parties', json=self.party)
        self.party['name'] = 'One name'
        res = self.client.post('/api/version1/parties', json=self.party)
        self.party['name'] = 'Another name'
        res = self.client.get('/api/version1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was successful')
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(res.status_code, 200)

    def test_get_parties_no_data(self):
        res = self.client.get('/api/version1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was successful')
        self.assertEqual(len(data['data']), 0)
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

    def test_get_party_id_not_found(self):
        res = self.client.get('/api/version1/parties/35')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Party not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)

    def test_edit_party(self):
        self.client.post('/api/version1/parties', json=self.party)

        res = self.client.patch('/api/version1/parties/1/PNU')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'PNU updated successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(data['data'][0]['name'], 'PNU')
        self.assertEqual(res.status_code, 200)

    def test_edit_party_id_not_found(self):
        res = self.client.get('/api/version1/parties/35')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Party not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)

    def test_delete_party(self):
        self.client.post('/api/version1/parties', json=self.party)

        res = self.client.delete('/api/version1/parties/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Kanu deleted successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_party_id_not_found(self):
        res = self.client.get('/api/version1/parties/35')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Party not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)
