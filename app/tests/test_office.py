from .skeleton_test import Skeleton
from app.version1.routes import offices

class TestOffice(Skeleton):

    def setUp(self):
        super().setUp()
        
        self.office = {
            "category": "National",
            "name": "President"
        }
    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        offices.clear()

    def test_create_office(self):
        res = self.client.post('/api/version1/offices', json = self.office)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Your political office was created successfully')
        self.assertEqual(res.status_code, 201)

   