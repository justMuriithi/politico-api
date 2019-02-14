from app.tests.v2.base_test import Base


class TestUsers(Base):

    def setUp(self):
        super().setUp()

        self.user = {
            "firstname": "Tony",
            "lastname": "Maina",
            "national_id": 5549260,
            "email": "Tony@demo.com",
            "isAdmin": True
        }

    # clear all lists after tests
    def tearDown(self):
        self.user['firstname'] = 'Tony'
        super().tearDown()

    # tests for POST auth/signup
    def test_register_user(self):
        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(res.status_code, 201)

    def test_register_user_email_exists(self):
        """ Tests that a user is not created twice with same email """

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(
            data['error'], 'A User with that email already exists')
        self.assertEqual(res.status_code, 400)

    def test_register_user_missing_fields(self):
        """ Tests when some fields are missing e.g firstname """

        res = self.client.post('/api/v2/auth/signup', json={
            "lastname": "Njoki"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'firstname field is required')
        self.assertEqual(res.status_code, 400)

    def test_register_user_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v2/auth/signup')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_register_user_int_name(self):
        """ Tests when integer is provided for firstname """

        self.user['firstname'] = 3
        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(
            data['error'], 'Integer types are not allowed for some fields')
        self.assertEqual(res.status_code, 400)

    def test_register_user_string_bool(self):
        """ Tests when bool is not provided for isAdmin """

        self.user['isAdmin'] = "true"
        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(
            data['error'], 'isAdmin is supposed to be a boolean value')
        self.assertEqual(res.status_code, 400)
