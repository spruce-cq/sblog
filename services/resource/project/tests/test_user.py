# services/resource/project/tests/test_users.py


import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_admin


class TestUserService(BaseTestCase):
    """Tests for users services"""

    def test_users(self):
        """Ensure the /ping route behaves correctly"""
        response = self.client.get('/users/ping')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    # add user
    def test_add_user_not_admin(self):
        """Ensure a new user can not be added to the database, when the
        user is not admin"""
        # flask._preserve_context to implement the deffered clearup
        # __exit__: request_ctx_stack.top.pop()
        add_user('test', 'test@qq.com', 'jianxin1234')
        response = self.client.post(
            '/auth/login',
            json={'email': 'test@qq.com', 'password': 'jianxin1234'}
        )
        token = response.get_json().get('auth_token')
        response = self.client.post(
            '/users',
            json={
                'username': 'jianxin',
                'email': 'jianxin@qq.com',
                'password': 'password1234'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertIn(
            data['message'],
            'You do not have permission to do that.')
        self.assertEqual('fail', data['status'])
        self.assertEqual(response.status_code, 403)

    def test_add_user_with_admin(self):
        add_admin('test', 'test@qq.com', 'jianxin1234')
        response = self.client.post(
            '/auth/login',
            json={'email': 'test@qq.com', 'password': 'jianxin1234'}
        )
        token = response.get_json().get('auth_token')
        response = self.client.post(
            '/users',
            json={
                'username': 'jianxin',
                'email': 'jianxin@qq.com',
                'password': 'password1234'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertIn(data['message'], 'jianxin@qq.com was added')
        self.assertEqual('success', data['status'])
        self.assertEqual(response.status_code, 201)

    def test_add_user_invalid_json_empty(self):
        """Ensure error is thrown if the json object is empty."""
        add_admin('test', 'test@qq.com', 'jianxin1234')
        response = self.client.post(
            '/auth/login',
            json={'email': 'test@qq.com', 'password': 'jianxin1234'}
        )
        token = response.get_json().get('auth_token')
        response = self.client.post(
            '/users', json={}, headers={'Authorization': f'Bearer {token}'})
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_no_username(self):
        """Ensure error is thrown if the json object doesn't have
        username key."""
        add_admin('test', 'test@qq.com', 'jianxin1234')
        response = self.client.post(
            '/auth/login',
            json={'email': 'test@qq.com', 'password': 'jianxin1234'}
        )
        token = response.get_json().get('auth_token')
        response = self.client.post(
            '/users',
            json={'eamil': 'jianxin@qq.com', 'password': 'password1234'},
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertIn('Invalid payload', data['message'])
        self.assertIn('fail', data['status'])
        self.assertEqual(response.status_code, 400)

    def test_add_user_invalid_json_no_password(self):
        """Ensure error is thrown if the json object doesn't have
        password key."""
        add_admin('test', 'test@qq.com', 'jianxin1234')
        response = self.client.post(
            '/auth/login',
            json={'email': 'test@qq.com', 'password': 'jianxin1234'}
        )
        token = response.get_json().get('auth_token')
        response = self.client.post(
            '/users',
            json={'eamil': 'jianxin@qq.com', 'username': 'jianxin'},
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email is already existing."""
        add_admin('test', 'test@qq.com', 'jianxin1234')
        response = self.client.post(
            '/auth/login',
            json={'email': 'test@qq.com', 'password': 'jianxin1234'}
        )
        token = response.get_json().get('auth_token')
        self.client.post(
            '/users',
            json={
                'username': 'jianxin',
                'email': 'jianxin@qq.com',
                'password': 'password1234'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        response = self.client.post(
            '/users',
            json={
                'username': 'jianxin',
                'email': 'jianxin@qq.com',
                'password': 'password1234'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('Sorry, the email is already existing.', data['message'])
        self.assertIn('fail', data['status'])

    # get single user
    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('jianxin', 'jianxin@qq.com', 'password1234')
        response = self.client.get(f'/users/{user.id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('jianxin', data['data']['username'])
        self.assertIn('jianxin@qq.com', data['data']['email'])
        self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        response = self.client.get('/users/jianxin')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('User does not exist', data['message'])
        self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        response = self.client.get('/users/999')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('User does not exist', data['message'])
        self.assertIn('fail', data['status'])

    # get all users
    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_admin('jianxin', 'jianxin@qq.com', 'password1234')
        add_user('changqing', 'changqing@qq.com', 'password1234')
        response = self.client.get('/users')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']['users']), 2)
        self.assertIn('jianxin', data['data']['users'][0]['username'])
        self.assertIn('jianxin@qq.com', data['data']['users'][0]['email'])
        self.assertTrue(data['data']['users'][0]['admin'])

        self.assertIn('changqing', data['data']['users'][1]['username'])
        self.assertIn('changqing@qq.com', data['data']['users'][1]['email'])
        self.assertIn('success', data['status'])
        self.assertFalse(data['data']['users'][1]['admin'])


if __name__ == '__main__':
    unittest.main()
