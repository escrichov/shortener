from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from shortener_app.models import ShortUrl


class ElementHasCSSClass():
    """An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(
            *self.locator) # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return element

        return False


class CommonTestCase(LiveServerTestCase):

    def setUp(self):
        settings.HOSTNAME = self.live_server_url

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('lang=en')

        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(1024, 768)
        self.wait = WebDriverWait(self.browser, 10)

    def tearDown(self):
        self.browser.quit()

    def get_url_by_index(self, url_index):
        return self.browser.find_elements_by_class_name('url-row')[url_index]


class NewVisitorTest(CommonTestCase):

    def test_can_shorten_a_url_and_retrieve_it_later(self):
        # Edith has heard about a cool new online Shotener app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention "Shortener" app
        self.assertIn('Shortener', self.browser.title)
        header_text = self.browser.find_element_by_xpath("//main//h1").text
        self.assertIn('Shortener', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_xpath(
            "//main//form//input[@name='url']")
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Shorten your url')

        # She types "https://news.ycombinator.com" into a text box (Edith's hobby
        # is read Hacker news)
        inputbox.send_keys('https://news.ycombinator.com')

        # When she hits enter, the page updates, and now the page lists
        # "https://news.ycombinator.com" as an item in a list table
        inputbox.send_keys(Keys.ENTER)
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'url-row')))

        header_text = self.browser.find_element_by_xpath("//main//h3").text
        self.assertIn('Your short url', header_text)

        real_url_button = self.get_url_by_index(0).find_elements_by_tag_name(
            'a')[1]

        self.assertEqual(real_url_button.text, 'https://news.ycombinator.com')

    def test_can_sign_up(self):
        # Edith has heard about a cool new online Shotener app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the "Sign up" button on the corner
        signup_button = self.browser.find_element_by_xpath(
            "//header//ul[2]//li[2]//a")
        self.assertIn('Sign up', signup_button.text)

        # When she clicks on the "Sign up button", the page updates and now appears a Sign up form
        signup_button.click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.XPATH, '//main//h1'),
                                             "Register"))

        # She fill the email and password
        sign_up_form = self.browser.find_element_by_xpath("//main//form")
        sign_up_form.find_element_by_name('email').send_keys(
            'edith@hispage.com')
        sign_up_form.find_element_by_name('password1').send_keys('fdfasd890')
        sign_up_form.find_element_by_name('password2').send_keys('fdfasd890')

        # When she hit click on the form, the page reloads, and now the Log in form appears
        sign_up_form.find_element_by_xpath("//button[@type='submit']").click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.XPATH, '//main//h2'), "Login"))


class LoginUserTest(CommonTestCase):

    def setUp(self):
        super().setUp()

        self.user = get_user_model().objects.create_user( # nosec
            email='edith@hispage.com', password='fdfasd890')

    def test_login(self):
        # Edith come back to Shortener app to login into her account
        self.browser.get('{}/accounts/login'.format(self.live_server_url))

        # She fill again the email and password on the form
        login_form = self.browser.find_element_by_xpath("//main//form")
        login_form.find_element_by_name('username').send_keys(
            'edith@hispage.com')
        login_form.find_element_by_name('password').send_keys('fdfasd890')

        # When she hit click on the form, the page reloads, and now edith can view
        # her personal space
        login_form.find_element_by_xpath("//button[@type='submit']").click()
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//header//ul//li[3]//a'), "Logout"))

    def test_login_invalid_password(self):
        # Edith come back to Shortener app to login into her account
        self.browser.get('{}/accounts/login'.format(self.live_server_url))

        # She fill again the email and a bad password on the form
        login_form = self.browser.find_element_by_xpath("//main//form")
        login_form.find_element_by_name('username').send_keys(
            'edith@hispage.com')
        login_form.find_element_by_name('password').send_keys('flass_onion')

        # When she hit click on the form, the page reloads
        login_form.find_element_by_xpath("//button[@type='submit']").click()
        self.wait.until(
            ElementHasCSSClass((By.XPATH, '//main//form//ul'), "errorlist"))

        # Now Edit she the error
        error_text = self.browser.find_element_by_xpath(
            "//main//form//ul//li").text
        self.assertIn(
            "Please enter a correct email and password. "
            "Note that both fields may be case-sensitive.", error_text)


class AccountBackendUserTest(CommonTestCase):

    def setUp(self):
        super().setUp()

        self.user = get_user_model().objects.create_user( # nosec
            email='edith@hispage.com', password='fdfasd890')
        self.client.force_login(self.user)
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value})

    def test_view_profile(self):
        # Edith come back to Shortener app, she is already logged in
        self.browser.get(self.live_server_url)

        # She views her profile in the header
        profile_button = self.browser.find_element_by_xpath(
            "//header//ul[2]//li[2]//a")
        self.assertIn('Profile', profile_button.text)

        # When she hit click on the profile button, the page reloads,
        # and now Edith can view her profile
        profile_button.click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.XPATH, '//main//h2'),
                                             "Email Address"))

    def test_view_my_urls(self):
        # Edith come back to Shortener app, she is already logged in
        self.browser.get(self.live_server_url)

        # She views "my urls" button in the header
        my_urls_button = self.browser.find_element_by_xpath(
            "//header//ul[2]//li[1]//a")
        self.assertIn('My urls', my_urls_button.text)

        # When she hit click on the profile button, the page reloads,
        # and now Edith can view her profile
        my_urls_button.click()
        self.wait.until(EC.url_to_be('{}/myurls'.format(self.live_server_url)))

    def test_create_url(self):

        # Edith come back to Shortener app, she is already logged in
        self.browser.get('{}/myurls'.format(self.live_server_url))

        # She is invited to enter a url item straight away
        inputbox = self.browser.find_element_by_xpath(
            "//main//form//input[@name='url']")
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Shorten your url')

        # She types "https://google.com" into a text box (Edith's hobby is search in Google)
        target_url = 'https://google.com'
        inputbox.send_keys(target_url)

        # When she hits enter, the page updates, and now the page lists
        # "https://google.com" as an item in a list table
        inputbox.send_keys(Keys.ENTER)

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, "//main//a[contains(@class, 'url-target-link')]"),
                target_url))

    def test_view_url_stats(self):
        # Create data
        short_url = ShortUrl()
        short_url.user = self.user
        short_url.target = 'https://google.com'
        short_url.save()

        # Edith come back to Shortener app, she is already logged in
        self.browser.get('{}/myurls'.format(self.live_server_url))

        # She views the "View stats" button in the first url
        stats_button = self.get_url_by_index(0).find_elements_by_tag_name(
            'a')[2]

        # When she hit click on the "View stats" button, the page redirect to Stats page
        stats_button.click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.XPATH, '//main//h3'), "Stats"))

    def test_delete_url(self):
        # Create data
        short_url = ShortUrl()
        short_url.user = self.user
        short_url.target = 'https://google.com'
        short_url.save()

        # Edith come back to Shortener app, she is already logged in
        self.browser.get('{}/myurls'.format(self.live_server_url))

        # She views the "Delete" button in the first url
        delete_button = self.get_url_by_index(0).find_element_by_xpath(
            './/form')

        # When she hit click on the "View stats" button, the page redirect to Stats page
        delete_button.click()
        self.wait.until(
            EC.invisibility_of_element_located((By.XPATH,
                                                '//main//table//tbody//tr[1]')))

    def test_follow_real_link(self):
        # Create data
        short_url = ShortUrl()
        short_url.user = self.user
        short_url.url = '{}/'.format(self.live_server_url)
        short_url.save()

        # Edith come back to Shortener app, she is already logged in
        self.browser.get('{}/myurls'.format(self.live_server_url))

        # She views the link in the first url
        real_url_button = self.get_url_by_index(0).find_elements_by_tag_name(
            'a')[1]

        # When she hit click on the url link button,
        # the page redirect to url
        real_url_button.click()
        self.wait.until(EC.url_to_be('{}/'.format(self.live_server_url)))

    def test_follow_short_link(self):
        # Create data
        short_url = ShortUrl()
        short_url.user = self.user
        short_url.url = '{}/'.format(self.live_server_url)
        short_url.save()

        # Edith come back to Shortener app, she is already logged in
        self.browser.get('{}/myurls'.format(self.live_server_url))

        # She views the "Short url" link in the first url
        short_url_button = self.get_url_by_index(0).find_elements_by_tag_name(
            'a')[1]
        self.assertEqual(short_url_button.text, short_url.url)

        # When she hit click on the "Short url" link, the page redirect to url
        short_url_button.click()
        self.wait.until(EC.url_to_be('{}/'.format(self.live_server_url)))

    def test_logout(self):
        # Edith come back to Shortener app, she is already logged in
        self.browser.get(self.live_server_url)

        # She views the "Logout" button in the header
        my_urls_button = self.browser.find_element_by_xpath(
            "//header//ul[2]//li[3]//a")
        self.assertIn('Logout', my_urls_button.text)

        # When she hit click on the "Logout" button, the page redirect to Homepage
        my_urls_button.click()
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//header//ul[2]//li[1]//a'), "Login"))
