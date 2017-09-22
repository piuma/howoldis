import app
import unittest
import os
import tempfile
from flask import url_for


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.app.test_client()
        self.app.testing = True


    def tearDown(self):
        """Clear DB after running tests"""
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])


    def test_home_status_code(self):
        """Assert that user successfully lands on homepage"""
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_todo_creation(self):
        """Assert that user is redirected after creating todo item"""
        response = self.app.post('/new',
                                 data=dict(name="First todo",
                                           description="Test todo")
                                 )
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
