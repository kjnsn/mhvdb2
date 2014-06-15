from mhvdb2 import app
from mhvdb2.resources import members, payments
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertTrue(rv.status_code == 200)

    def test_signup_get(self):
        rv = self.app.get('/signup/')
        self.assertTrue(rv.status_code == 200)

    def test_signup_post(self):
        rv = self.app.post('/signup/', data={
            "name": "Foo Bar",
            "email": "foobar@example.com",
            "phone": "123456789",
            "agree": "true"},
            follow_redirects=True)

        self.assertTrue(rv.status_code == 200)

        # Invalid email, should return invalid
        rv = self.app.post('/signup/', data={
            "name": "foobar",
            "email": "foobar",
            "phone": "123456789",
            "agree": "true"},
            follow_redirects=True)

        self.assertTrue(rv.status_code == 400)

        rv = self.app.post('/signup/', follow_redirects=True)
        self.assertTrue(rv.status_code == 400)

    def test_payment_get(self):
        rv = self.app.get('/signup/')
        self.assertTrue(rv.status_code == 200)

    def test_payment_post(self):
        # Make sure there is a signed up user
        rv = self.app.post('/signup/', data={
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "123456789",
            "agree": "true"},
            follow_redirects=True)

        rv = self.app.post('/payments/', data={
            "amount": 12.10,
            "email": "alice@example.com",
            "method": 0,
            "type": 0,
            "notes": "This is my first payment",
            "reference": "alice"},
            follow_redirects=True)

        self.assertTrue(rv.status_code == 200)

        # Invalid email, should return invalid
        rv = self.app.post('/signup/', data={
            "first-name": "Foobar",
            "last-name": "foobar",
            "email": "foobar",
            "phone": "123456789",
            "agree": "true"},
            follow_redirects=True)

        self.assertTrue(rv.status_code == 400)

        rv = self.app.post('/signup/', follow_redirects=True)
        self.assertTrue(rv.status_code == 400)

    def test_payment_validation(self):
        # Make sure there is a signed up user
        rv = self.app.post('/signup/', data={
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "123456789",
            "agree": "true"},
            follow_redirects=True)

        # amount, email, method, type, notes, reference
        errors = payments.validate("12", "alice@example.com", "0", "0", "", "vjhfg")
        self.assertEqual(errors, [])
        
        errors = payments.validate("12.45", "alice@example.com", "0", "0", "", "vjhfg")
        self.assertEqual(errors, [])
        
        errors = payments.validate("12.101", "alice@example.com", "0", "0", "", "vjhfg")
        self.assertTrue(len(errors) > 0)


if __name__ == '__main__':
    unittest.main()
