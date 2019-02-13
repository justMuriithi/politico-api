from base_test import Base
from app.v2.models.db import Database

class TestOffice(Base):

    def setUp(self):
        super().setUp()

        self.offices = Database().get_table(Database.OFFICES)
  
        self.office = {
            "category": "National",
            "name": "President"
        }
    # clear all lists after tests
    def tearDown(self):
        super().tearDown()

    def test_create_office(self):
        res = self.client.post('/api/v2/offices', json = self.office)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Your political office was created successfully')
        self.assertEqual(res.status_code, 201)

    def test_create_office_name_exists(self):
        self.client.post('/api/v2/offices', json=self.office)
        res = self.client.post('/api/v2/offices', json=self.office)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Office already exists')
        self.assertEqual(res.status_code, 400)

    def test_create_office_missing_fields(self):
        res = self.client.post('/api/v2/offices', json={
            "category": "National"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'name field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_office_no_data(self):
        res = self.client.post('/api/v2/offices')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_get_offices(self):
        res = self.client.post('/api/v2/offices', json = self.office)
        self.office['name'] = 'One name'
        res = self.client.post('/api/v2/offices', json = self.office)
        self.office['name'] = 'Another name'

        res = self.client.get('/api/v2/offices')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was successful')
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(res.status_code, 200)
    
    def test_get_offices_no_data(self):
        res = self.client.get('/api/v2/offices')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was successful')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    def test_get_office(self):
        self.client.post('/api/v2/offices', json = self.office)

        res = self.client.get('/api/v2/offices/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was successful')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_office_id_not_found(self):
        res = self.client.get('/api/v2/offices/35')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Office not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)
