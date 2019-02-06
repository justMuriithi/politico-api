from .test_skeleton import Skeleton
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

    
