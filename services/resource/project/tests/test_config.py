# services/resource/project/tests/test_config.py


import os
import unittest

from flask import current_app

from project import create_app


class TestDevelopmentConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')

    def test_app_is_development(self):
        self.assertTrue(
            self.app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY'))
        self.assertFalse(current_app is None)
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_DEV_URL')
        )
        self.assertTrue(self.app.config['BCRYPT_LOG_ROUNDS'] == 4)
        self.assertTrue(self.app.config['TOKEN_EXPIRATION_DAYS'] == 30)
        self.assertTrue(self.app.config['TOKEN_EXPIRATION_SECONDS'] == 0)


class TestTestingConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

    def test_app_is_testing(self):
        self.assertTrue(
            self.app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY'))
        self.assertTrue(self.app.config['TESTING'])
        self.assertFalse(self.app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )
        self.assertTrue(self.app.config['BCRYPT_LOG_ROUNDS'] == 4)
        self.assertTrue(self.app.config['TOKEN_EXPIRATION_DAYS'] == 0)
        self.assertTrue(self.app.config['TOKEN_EXPIRATION_SECONDS'] == 3)


class TestProductionConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('production')

    def test_app_is_production(self):
        self.assertTrue(
            self.app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY'))
        self.assertFalse(self.app.config['TESTING'])
        self.assertTrue(self.app.config['BCRYPT_LOG_ROUNDS'] == 13)
        self.assertTrue(self.app.config['TOKEN_EXPIRATION_DAYS'] == 30)
        self.assertTrue(self.app.config['TOKEN_EXPIRATION_SECONDS'] == 0)


if __name__ == '__main__':
    unittest.main()
