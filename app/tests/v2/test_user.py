from .base_test import Base


class TestUsers(Base):

    def setUp(self):
        super().setUp()

        self.user = {
            "firstname": "John",
            "lastname": "Maina",
            "national_id": "333333",
            "email": "johndoe@gmail.com",
            "admin": True,
            "password": "nimimi"
        }

    # clear all lists after tests
    def tearDown(self):
        self.user['firstname'] = 'John'
        super().tearDown()

    # tests for POST auth/signup
    def test_register_user(self):
        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(data['data'][0]['user']['firstname'], 'John')
        self.assertIn('token', data['data'][0])
        self.assertEqual(res.status_code, 201)

    def test_register_user_email_exists(self):
        """ Tests that a user is not created twice with same email """

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(data['status'], 409)
        self.assertEqual(
            data['error'], 'A User with that email already exists')
        self.assertEqual(res.status_code, 409)

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
        """ Tests when Invalid or empty string is provided for firstname """

        self.user['firstname'] = 3
        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(
            data['error'], 'Invalid or empty string')
        self.assertEqual(res.status_code, 400)

    def test_register_user_invalid_email(self):
        """ Tests when invalid email is provided """

        self.user['email'] = 'check'
        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Invalid email')
        self.assertEqual(res.status_code, 400)

    # tests for login
    def test_login_user(self):
        """ Tests that a user was loged in successfully """

        res = self.client.post('/api/v2/auth/login', json={
            'email': 'antoineshephmaina@gmail.com',
            'password': 'nimimi'
        })
        data = res.get_json()

        self.assertEqual(data['message'], 'Success')
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['data'][0]['user']['firstname'], 'Tony')
        self.assertIn('token', data['data'][0])
        self.assertEqual(res.status_code, 200)

    def test_login_missing_email(self):
        """ Tests when some fields are missing e.g email """

        res = self.client.post('/api/v2/auth/login', json={
            "password": "nimimi"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'email field is required')
        self.assertEqual(res.status_code, 400)

    def test_login_missing_password(self):
        """ Tests when some fields are missing e.g password """

        res = self.client.post('/api/v2/auth/login', json={
            "email": "antoineshephmaina@gmail.com"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'password field is required')
        self.assertEqual(res.status_code, 400)

    def test_login_no_user(self):
        """ Tests when user is not registered """

        res = self.client.post('/api/v2/auth/login', json={
            "email": "shephmaina@gmail.com",
            "password": "password"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'User not registered')
        self.assertEqual(res.status_code, 404)

    def test_login_incorrect_password(self):
        """ Tests when user is not registered """

        res = self.client.post('/api/v2/auth/login', json={
            "email": "antoineshephmaina@gmail.com",
            "password": "password"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 401)
        self.assertEqual(data['error'], 'Incorrect password')
        self.assertEqual(res.status_code, 401)

    def test_login_not_valid_email(self):
        """ Tests when an invalid email is provided for login """

        res = self.client.post('/api/v2/auth/login', json={
            "email": "tryzx",
            "password": "validpassword"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 422)
        self.assertEqual(data['error'], 'Please provide a valid email')
        self.assertEqual(res.status_code, 422)

    # test reset password
    def test_reset_password_no_email(self):
        """ Tests when some fields are missing e.g email """

        res = self.client.post('/api/v2/auth/reset', json={
            "password": "nimimi"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'email field is required')
        self.assertEqual(res.status_code, 400)

    def test_reset_password_invalid_email(self):
        """ Tests when some fields are missing e.g email """

        res = self.client.post('/api/v2/auth/reset', json={
            "email": "tryzx"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 422)
        self.assertEqual(data['error'], 'Please provide a valid email')
        self.assertEqual(res.status_code, 422)

    def test_reset_password_no_user(self):
        """ Tests when user does not exist"""

        res = self.client.post('/api/v2/auth/reset', json={
            "email": "wadahuhu@gmail.com"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'User not found')
        self.assertEqual(res.status_code, 404)

    def test_reset_password_no_data(self):
        """ Tests when no data is provided"""

        res = self.client.post('/api/v2/auth/reset')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_reset_password(self):
        """ Tests reset password """

        res = self.client.post('/api/v2/auth/reset', json={
            "email": "antoineshephmaina@gmail.com"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(
            data['data'][0]['message'],
            'Check your email for password reset link')
        self.assertEqual(res.status_code, 200)

    # change password
    def test_change_password(self):
        """ Tests when some fields are missing e.g email """

        res = self.client.post('/api/v2/reset-password', json={
            "password": "nimimi"
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(
            data['data'][0]['message'],
            'Your password has been updated')
        self.assertEqual(res.status_code, 200)

        res = self.client.post('/api/v2/auth/login', json={
            'email': 'antoineshephmaina@gmail.com',
            'password': 'nimimi'
        })
        data = res.get_json()

        self.assertEqual(data['message'], 'Success')
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['data'][0]['user']['firstname'], 'Tony')
        self.assertIn('token', data['data'][0])
        self.assertEqual(res.status_code, 200)

    def test_change_password_short(self):
        """ Tests when some fields are missing e.g email """

        res = self.client.post('/api/v2/reset-password', json={
            "password": "try"
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 422)
        self.assertEqual(
            data['error'],
            'Password must be at least 6 characters long')
        self.assertEqual(res.status_code, 422)

    def test_change_password_no_data(self):
        """ Tests when some fields are missing e.g email """

        res = self.client.post('/api/v2/reset-password', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(
            data['error'],
            'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_change_password_no_password(self):
        """ Tests when some fields are missing e.g email """

        res = self.client.post('/api/v2/reset-password', json={
            "email": "nani"
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(
            data['error'],
            'password field is required')
        self.assertEqual(res.status_code, 400)
