# services/resource/project/tests/test_category.py


import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import get_token, add_category


class TestCategoryService(BaseTestCase):
    """Test for category service."""

    def test_add_category_with_user(self):
        token = get_token(self.client)
        response = self.client.post(
            '/categories',
            json={'name': 'category-one'},
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['message'], 'category: category-one was added.')
        self.assertEqual(data['status'], 'success')
        self.assertEqual(response.status_code, 201)

    def test_add_category_without_user(self):
        response = self.client.post(
            '/categories',
            json={'name': 'category-one'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(
            data['message'], 'Invalid payload. Please log in again.')
        self.assertEqual(response.status_code, 403)

    def test_add_category_no_name(self):
        token = get_token(self.client)
        response = self.client.post(
            '/categories',
            json={},
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid payload.')
        self.assertEqual(response.status_code, 400)

    def test_get_all_categories(self):
        add_category('category-one')
        add_category('category-two')
        response = self.client.get('/categories')
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data'][0]['name'], 'category-one')

    def test_get_single_category(self):
        add_category('category-one')
        add_category('category-two')
        response = self.client.get('/categories/1')
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], 1)
        self.assertEqual(data['data']['name'], 'category-one')
        self.assertEqual(response.status_code, 200)

    def test_get_single_category_incorrect_id(self):
        add_category('category-one')
        add_category('category-two')
        response = self.client.get('/categories/3')
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid payload.')
        self.assertEqual(response.status_code, 404)

    def test_get_single_category_invalid_id(self):
        add_category('category-one')
        add_category('category-two')
        response = self.client.get('/categories/jianxin')
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid payload.')
        self.assertEqual(response.status_code, 400)

    def test_delete_category(self):
        add_category('category-one')
        add_category('category-two')
        token = get_token(self.client)
        response = self.client.delete(
            '/categories/1',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('category-one is already deleted.', data['message'])
        self.assertEqual(response.status_code, 202)

    def test_delete_category_incorrect_id(self):
        add_category('category-one')
        add_category('category-two')
        token = get_token(self.client)
        response = self.client.delete(
            '/categories/3',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertIn('Invalid payload.', data['message'])
        self.assertEqual(response.status_code, 404)

    def test_delete_category_invalid_id(self):
        add_category('category-one')
        add_category('category-two')
        token = get_token(self.client)
        response = self.client.delete(
            '/categories/jianxin',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertIn('Invalid payload.', data['message'])
        self.assertEqual(response.status_code, 400)

    def test_delete_category_without_user(self):
        add_category('category-one')
        add_category('category-two')
        response = self.client.delete('/categories/jianxin')
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertIn('Invalid payload. Please log in again.', data['message'])
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
