from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Create your tests here.
class LoginFormTest(LiveServerTestCase):

    def test_login_form(self):
        # Change this to your preferred driver assuming it is installed
        selenium = webdriver.Firefox()
        # Set up the url to visit
        selenium.get('http://127.0.0.1:8000/users/accounts/login/')
        # find the elements you need to using ids
        username = selenium.find_element('id_username')
        password = selenium.find_element('id_password')

        # get Login button by using id_login
        submit = selenium.find_element('id_login')

        # Add/populate data to the form
        username.send_keys('test4')
        password.send_keys('lavieestbelle')

        # submit form
        submit.send_keys(Keys.RETURN)

        # Page source looks at the html page
        assert 'test4' in selenium.page_source
