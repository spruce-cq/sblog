# services/resource/project/tests/test_auth.py


import unittest

from flask import current_app

from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAuthPaint(BaseTestCase):

    def test_user_registration(self):
        response = self.client.post(
            '/auth/register',
            json={
                'username': 'jianxin',
                'email': 'jianxin@qq.com',
                'password': 'password1234'
            }
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'success')
        self.assertIn('Successfully registered.', data['message'])
        self.assertTrue(data['auth_token'])

    def test_user_registration_duplicate_email(self):
        add_user('jianxin', 'jianxin@qq.com', 'jianxin')
        response = self.client.post(
            '/auth/register',
            json={
                'username': 'changqing',
                'email': 'jianxin@qq.com',
                'password': 'changiqng1234'
            }
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('Sorry, that user already existing.', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_duplicate_username(self):
        add_user('jianxin', 'jianxin@qq.com', 'jianxin')
        response = self.client.post(
            '/auth/register',
            json={
                'username': 'jianxin',
                'email': 'changqing@qq.com',
                'password': 'changiqng1234'
            }
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('Sorry, that user already existing.', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json(self):
        response = self.client.post('/auth/register', json={})
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_no_username(self):
        response = self.client.post(
            '/auth/register',
            json={
                'email': 'jianxin@qq.com',
                'password': 'jianxin123'
            }
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_no_email(self):
        response = self.client.post(
            '/auth/register',
            json={
                'username': 'jianxin',
                'password': 'jianxin123'
            }
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_no_password(self):
        response = self.client.post(
            '/auth/register',
            json={
                'email': 'jianxin@qq.com',
                'username': 'jianxin'
            }
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data['message'])
        self.assertIn('fail', data['status'])

    def test_registered_user_login(self):
        add_user('jianxin', 'jianxin@qq.com', 'jianxin1234')
        response = self.client.post(
            'auth/login',
            json={
                'email': 'jianxin@qq.com',
                'password': 'jianxin1234'
            }
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertIn('Successfully logged in.', data['message'])
        self.assertTrue(data['auth_token'])

    def test_no_registered_user_login(self):
        response = self.client.post(
            'auth/login',
            json={
                'email': 'jianxin@qq.com',
                'password': 'jianxin1234'
            }
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('fail', data['status'])
        self.assertIn('User does not exists', data['message'])
        self.assertFalse(data.get('auth_token'))

    def test_valid_logout(self):
        add_user('jianxin', 'jianxin@qq.com', 'jianxin1234')
        login_response = self.client.post(
            '/auth/login',
            json={
                'email': 'jianxin@qq.com',
                'password': 'jianxin1234'
            }
        )
        token = login_response.get_json().get('auth_token')
        response = self.client.get(
            '/auth/logout',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        data = response.get_json()
        self.assertIn('Successfully logged out', data['message'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_invalid_logout_expired_token(self):
        add_user('jianxin', 'jianxin@qq.com', 'jianxin1234')
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        login_response = self.client.post(
            '/auth/login',
            json={
                'email': 'jianxin@qq.com',
                'password': 'jianxin1234'
            }
        )
        token = login_response.get_json().get('auth_token')
        response = self.client.get(
            '/auth/logout',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['status'], 'fail')
        self.assertTrue(
            data['message'] == 'Signature expired. Please log in again.')

    def test_invalid_logout_bad_token(self):
        response = self.client.get(
            '/auth/logout',
            headers={'Authorization': 'Bearer invalidtoken'}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'Invalid token. Please log in again.')

    def test_invalid_logout_no_authorization_header(self):
        response = self.client.get('/auth/logout')
        data = response.get_json()
        self.assertTrue(response.status_code == 403)
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'Invalid payload. Please log in again.')

    def test_user_status(self):
        add_user('test', 'test@test.com', 'test1234')
        login_resp = self.client.post(
            '/auth/login',
            json={
                'email': 'test@test.com',
                'password': 'test1234'
            }
        )
        token = (login_resp.get_json()).get('auth_token')
        response = self.client.get(
            '/auth/status',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['data'] is not None)
        self.assertTrue(data['data']['username'] == 'test')
        self.assertTrue(data['data']['email'] == 'test@test.com')
        self.assertFalse(data['data']['admin'])
        self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        response = self.client.get(
            '/auth/status',
            headers={'Authorization': 'Bearer invalid'})
        data = response.get_json()
        self.assertTrue(data['status'] == 'fail')
        self.assertIn(data['message'], 'Invalid token. Please log in again.')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
