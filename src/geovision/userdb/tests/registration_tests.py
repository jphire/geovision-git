
from django.test import TestCase
from django.test import Client
from django import template
from django.db.models import get_model

def template_names(response):
	for t in response.templates:
		yield t.name

class RegistrationTests(TestCase):

    #fixtures = ["userdb_testmaker"]


    def test_index_page_loads(self):
        r = self.client.get('/', {})
        self.assertEqual(r.status_code, 200)
	self.assertIn('login.html', template_names(r))
    def test_register_page_loads(self):
        r = self.client.get('/register', {})
        self.assertEqual(r.status_code, 200)
	self.assertIn('register.html', template_names(r))
    def test_registering_empty_username(self):
        r = self.client.post('/registering', {'username': '', 'password1': 'abc', 'password2': 'abc', 'firstname': 'abc', 'lastname': 'abc', 'csrfmiddlewaretoken': '380af29ce1b6e7b00f6a0aa750e48dc8', 'email': 'abc@abc.abc', })
	self.assertNotContains(r, 'Account succesfully created')
    def test_registering_different_passwords(self):
        r = self.client.post('/registering', {'username': 'def', 'password1': 'def', 'password2': 'ghi', 'firstname': 'def', 'lastname': 'def', 'csrfmiddlewaretoken': '380af29ce1b6e7b00f6a0aa750e48dc8', 'email': 'def', })
	self.assertContains(r, 'Error: Passwords did not match.')
    def test_registering_succesful(self):
        r = self.client.post('/registering', {'username': 'def', 'password1': 'def', 'password2': 'def', 'firstname': 'def', 'lastname': 'def', 'csrfmiddlewaretoken': '380af29ce1b6e7b00f6a0aa750e48dc8', 'email': 'def', })
	self.assertContains(r,'Account succesfully created')
    def test_register_twice(self):
        r = self.client.post('/registering', {'username': 'def', 'password1': 'def', 'password2': 'def', 'firstname': 'def', 'lastname': 'def', 'csrfmiddlewaretoken': '380af29ce1b6e7b00f6a0aa750e48dc8', 'email': 'def', })
        r = self.client.post('/registering', {'username': 'def', 'password1': 'xyz', 'password2': 'xyz', 'firstname': 'xyz', 'lastname': 'xyz', 'csrfmiddlewaretoken': '380af29ce1b6e7b00f6a0aa750e48dc8', 'email': 'xyz', })
	self.assertEqual(r.status_code, 200)
    def test_logging_in_nonexistent_user(self):
        r = self.client.post('/logging_in', {'username': 'quux', 'csrfmiddlewaretoken': '380af29ce1b6e7b00f6a0aa750e48dc8', 'password': 'quux', })
	self.assertContains(r, 'The username or password was incorrect')
    def test_logging_in_wrong_password(self):
	self.test_registering_succesful()
        r = self.client.post('/logging_in', {'username': 'def', 'csrfmiddlewaretoken': '380af29ce1b6e7b00f6a0aa750e48dc8', 'password': "' OR 1=1;--", })
	self.assertContains(r, 'The username or password was incorrect')
    def test_logging_in_succesfully(self):
	self.test_registering_succesful()
        r = self.client.post('/logging_in', {'username': 'def', 'csrfmiddlewaretoken': '380af29ce1b6e7b00f6a0aa750e48dc8', 'password': 'def', })
	self.assertNotContains(r, 'The username or password was incorrect')
