from .base_test import Base


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
            "email": "antoineshephmaina@gmail.com",
            "isAdmin": True
        }
        self.client.post('/api/v2/offices', json=self.office,
                         headers=self.headers)
        self.client.post('/api/v2/parties', json=self.party,
                         headers=self.headers)
        self.client.post('/api/v2/auth/login', json=self.user,
                         headers=self.headers)
        self.client.post('/api/v2/offices/register', json=self.candidate,
                         headers=self.headers)

    # clear all lists after tests
    def tearDown(self):
        self.vote['candidate'] = 1
        super().tearDown()

    # tests for POST votes
    def test_vote(self):
        """ Tests that a vote was created successfully """

        res = self.client.post('/api/v2/votes', json=self.vote,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(res.status_code, 201)

    def test_vote_missing_fields(self):
        """ Tests when some fields are missing e.g office """

        res = self.client.post('/api/v2/votes', json={
            "candidate": 1,
            "createdBy": 1
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'office field is \
            required')
        self.assertEqual(res.status_code, 400)

    def test_vote_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v2/votes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_create_vote_office_not_exist(self):
        """ Tests when the office does not exist  """

        res = self.client.post('/api/v2/votes', json={
            "office": 34,
            "createdBy": 1,
            "candidate": 1
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Selected Office does not exist')
        self.assertEqual(res.status_code, 404)

    def test_create_vote_candidate_not_exist(self):
        """ Tests when the user does not exist  """

        res = self.client.post('/api/v2/votes', json={
            "createdBy": 1,
            "office": 1,
            "candidate": 62
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Selected User does not exist')
        self.assertEqual(res.status_code, 404)

    def test_vote_twice(self):
        """ Tests when user attempts to vote twice for same office """

        self.client.post('/api/v2/votes', json=self.vote, headers=self.headers)
        res = self.client.post('/api/v2/votes', json=self.vote,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 409)
        self.assertEqual(data['error'], 'You can only vote once per office')
        self.assertEqual(res.status_code, 409)

    # tests for GET votes
    def test_get_all_votes(self):
        res = self.client.post('/api/v2/votes', json=self.vote,
                               headers=self.headers)

        res = self.client.get('/api/v2/votes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_all_votes_no_data(self):
        res = self.client.get('/api/v2/votes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    def test_get_all_user_votes(self):
        self.client.post('/api/v2/votes', json=self.vote, headers=self.headers)
        res = self.client.get('/api/v2/votes/candidate/1',
                              headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_all_office_votes(self):
        self.client.post('/api/v2/votes', json=self.vote, headers=self.headers)
        res = self.client.get('/api/v2/offices/1/result', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)
