from app.tests.version1.base_test import Base


class TestVote(Base):
    def setUp(self):
        super().setUp()

        self.vote = {
            "createdBy": 1,
            "office": 1,
            "candidate": 1
        }
        self.candidate = {
            "party": 1,
            "office": 1,
            "candidate": 1
        }
        self.party = {
            "name": "Kanu",
            "hqAddress": "Eldoret"
        }
        self.office = {
            "category": "National",
            "name": "President"
        }
        self.user = {
            "firstname": "Tony",
            "lastname": "Maina",
            "national_id": "5549260",
            "email": "Tony@demo.com",
            "isAdmin": True
        }
        self.client.post('/api/version1/offices', json=self.office)
        self.client.post('/api/version1/parties', json=self.party)
        self.client.post('/api/version1/auth/login', json=self.user)
        self.client.post(
            '/api/version1/offices/office-id/register', json=self.candidate)

    # clear all lists after tests
    def tearDown(self):
        self.vote['candidate'] = 1
        super().tearDown()

    # tests for POST votes
    def test_vote(self):
        """ Tests that a vote was created successfully """

        res = self.client.post('/api/version1/votes', json=self.vote)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(res.status_code, 201)

    def test_vote_missing_fields(self):
        """ Tests when some fields are missing e.g office """

        res = self.client.post('/api/version1/votes', json={
            "candidate": 1,
            "createdBy": 1
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'office field is required')
        self.assertEqual(res.status_code, 400)

    def test_vote_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/version1/votes')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_vote_twice(self):
        """ Tests when user attempts to vote twice for same office """

        self.client.post('/api/version1/votes', json=self.vote)
        res = self.client.post('/api/version1/votes', json=self.vote)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'You can only vote once per office')
        self.assertEqual(res.status_code, 400)

    # tests for GET votes
    def test_get_all_votes(self):
        res = self.client.post('/api/version1/votes', json=self.vote)

        res = self.client.get('/api/version1/votes')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_all_votes_no_data(self):
        res = self.client.get('/api/version1/votes')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    def test_get_all_user_votes(self):
        self.client.post('/api/version1/votes', json=self.vote)
        res = self.client.get('/api/version1/votes/user/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_all_office_votes(self):
        self.client.post('/api/version1/votes', json=self.vote)
        res = self.client.get('/api/version1/votes/office/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)
