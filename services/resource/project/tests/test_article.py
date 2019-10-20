# services/resource/project/tests/test_article.py


import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import get_token, add_category, add_article
from project.api.blog.models import Article


class TestArticleService(BaseTestCase):
    """Test for article service."""

    def test_add_article_with_user(self):
        add_category('default')
        token = get_token(self.client)
        response = self.client.post(
            '/articles',
            json={
                'title': 'test title',
                'body': 'test body.',
                'category': 1
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'article: test title was added.')
        self.assertEqual(response.status_code, 201)

    def test_add_article_without_user(self):
        add_category('default')
        response = self.client.post(
            '/articles',
            json={
                'title': 'test title',
                'body': 'test body.',
                'category': 1
            },
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(
            data['message'], 'Invalid payload. Please log in again.')
        self.assertEqual(response.status_code, 403)

    def test_add_article_no_title(self):
        add_category('default')
        token = get_token(self.client)
        response = self.client.post(
            '/articles',
            json={
                'body': 'test body.',
                'category': 1
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid payload.')
        self.assertEqual(response.status_code, 400)

    def test_add_article_no_body(self):
        add_category('default')
        token = get_token(self.client)
        response = self.client.post(
            '/articles',
            json={
                'title': 'test title',
                'category': 1
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid payload.')
        self.assertEqual(response.status_code, 400)

    def test_add_article_no_category(self):
        add_category('default')
        token = get_token(self.client)
        response = self.client.post(
            '/articles',
            json={
                'title': 'test title',
                'body': 'test body'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'article: test title was added.')
        self.assertEqual(response.status_code, 201)

    def test_get_all_article(self):
        cate1 = add_category('default')
        cate2 = add_category('test')
        add_article('default title', 'default body', cate1)
        add_article('test title', 'test body', cate2)

        response = self.client.get('/articles')
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data'][0]['title'], 'default title')
        self.assertEqual(data['data'][0]['body'], 'default body')
        self.assertIsInstance(data['data'][0]['id'], int)
        self.assertIsInstance(data['data'][0]['category'][0], int)
        self.assertEqual(data['data'][0]['category'][1], 'default')
        self.assertTrue(data['data'][0]['timestamp'])
        self.assertEqual(data['data'][1]['title'], 'test title')
        self.assertEqual(data['data'][1]['body'], 'test body')
        self.assertIsInstance(data['data'][1]['id'], int)
        self.assertIsInstance(data['data'][1]['category'][0], int)
        self.assertEqual(data['data'][1]['category'][1], 'test')
        self.assertTrue(data['data'][1]['timestamp'])
        self.assertEqual(response.status_code, 200)

    def test_get_single_article(self):
        cate1 = add_category('default')
        article = add_article('test title', 'test body', cate1)
        response = self.client.get(f'/articles/{article.id}')
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], article.id)
        self.assertEqual(data['data']['title'], article.title)
        self.assertEqual(data['data']['body'], article.body)
        self.assertTrue(data['data']['timestamp'])
        self.assertEqual(data['data']['category'][0], cate1.id)
        self.assertEqual(data['data']['category'][1], cate1.name)
        self.assertEqual(response.status_code, 200)

    def test_get_single_article_incorrect_id(self):
        cate1 = add_category('default')
        add_article('test title', 'test body', cate1)
        response = self.client.get(f'/articles/3')
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid path params.')
        self.assertEqual(response.status_code, 404)

    def test_get_single_article_invalid_id(self):
        cate1 = add_category('default')
        add_article('test title', 'test body', cate1)
        response = self.client.get(f'/articles/jianxin')
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid path params.')
        self.assertEqual(response.status_code, 404)

    def test_delete_single_article(self):
        cate = add_category('default')
        article = add_article('default title', 'default body', cate)
        token = get_token(self.client, admin=True)
        response = self.client.delete(
            f'/articles/{article.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(
            data['message'],
            f'{article.id}: {article.title} is already deleted.')
        self.assertEqual(response.status_code, 202)

    def test_delete_single_article_incorrect_id(self):
        cate = add_category('default')
        article = add_article('default title', 'default body', cate)
        token = get_token(self.client, admin=True)
        response = self.client.delete(
            f'/articles/{article.id + 1}',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid path params.')
        self.assertEqual(response.status_code, 404)

    def test_delete_single_article_without_user(self):
        cate = add_category('default')
        article = add_article('default title', 'default body', cate)
        response = self.client.delete(
            f'/articles/{article.id}',
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(
            data['message'], 'Invalid payload. Please log in again.')
        self.assertEqual(response.status_code, 403)

    def test_update_single_article(self):
        cate1 = add_category('default')
        cate2 = add_category('test')
        article = add_article('title', 'body', cate1)
        token = get_token(self.client)
        response = self.client.put(
            '/articles',
            json={
                'aid': f'{article.id}',
                'title': 'new title',
                'body': 'new body',
                'category': f'{cate2.id}'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(
            data['message'], f'{article.id}: article is already updated.')
        self.assertEqual(response.status_code, 200)

    def test_update_single_article_without_user(self):
        cate1 = add_category('default')
        cate2 = add_category('test')
        article = add_article('title', 'body', cate1)
        response = self.client.put(
            '/articles',
            json={
                'aid': f'{article.id}',
                'title': 'new title',
                'body': 'new body',
                'category': f'{cate2.id}'
            },
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(
            data['message'], 'Invalid payload. Please log in again.')
        self.assertEqual(response.status_code, 403)

    def test_udpate_single_article_no_aid(self):
        cate1 = add_category('default')
        cate2 = add_category('test')
        add_article('title', 'body', cate1)
        token = get_token(self.client)
        response = self.client.put(
            '/articles',
            json={
                'title': 'new title',
                'body': 'new body',
                'category': f'{cate2.id}'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid payload.')
        self.assertEqual(response.status_code, 404)

    def test_udpate_single_article_no_title(self):
        cate1 = add_category('default')
        cate2 = add_category('test')
        article = add_article('title', 'body', cate1)
        token = get_token(self.client)
        response = self.client.put(
            '/articles',
            json={
                'aid': f'{article.id}',
                'body': 'new body',
                'category': f'{cate2.id}'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['message'], 'Invalid payload.')
        self.assertEqual(response.status_code, 400)

    def test_update_single_article_no_category(self):
        add_category('default')
        cate2 = add_category('test')
        article = add_article('title', 'body', cate2)
        token = get_token(self.client)
        response = self.client.put(
            '/articles',
            json={
                'aid': f'{article.id}',
                'title': 'new title',
                'body': 'new body',
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(
            data['message'], f'{article.id}: article is already updated.')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.query.get(article.id).category.id, 1)


if __name__ == "__main__":
    unittest.main()
