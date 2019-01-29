from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.test import APITestCase
from rest_framework import status

from shortener_app.serializers import ShortUrlSerializer
from shortener_app.models import APIAccess, ShortUrl


class APITests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='edith@hispage.com', password='fdfasd890')
        self.api_access = APIAccess()
        self.api_access.user = self.user
        self.api_access.save()

        self.header_name = 'HTTP_X_API_KEY'
        self.headers = {self.header_name: self.api_access.apikey}

    def assert_authentication_failed(self, response):
        self.assertEqual(
            response.data,
            {'detail': exceptions.AuthenticationFailed('No such user').detail}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assert_response_ok(self, response, expected_data):
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_list_authentication_error(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('shortener_app:api_list_urls')
        self.headers = {self.header_name: 'invalid-api-key'}

        response = self.client.get(url, format='json', **self.headers)

        self.assert_authentication_failed(response)

    def test_url_list_empty(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('shortener_app:api_list_urls')

        response = self.client.get(url, format='json', **self.headers)

        self.assert_response_ok(response, [])

    def test_url_list_only_my_urls(self):
        """
        Ensure we can create a new account object.
        """
        others_url_short_url = ShortUrl()
        others_url_short_url.url = 'https://www.google.com'
        others_url_short_url.user = None
        others_url_short_url.save()
        my_short_url = ShortUrl()
        my_short_url.url = 'https://es.yahoo.com'
        my_short_url.user = self.user
        my_short_url.save()

        s = ShortUrlSerializer([my_short_url], many=True)

        url = reverse('shortener_app:api_list_urls')
        response = self.client.get(url, format='json', **self.headers)

        self.assert_response_ok(response, s.data)

    def test_url_list(self):
        """
        Ensure we can create a new account object.
        """
        short_url_1 = ShortUrl()
        short_url_1.url = 'https://www.google.com'
        short_url_1.user = self.user
        short_url_1.save()
        short_url_2 = ShortUrl()
        short_url_2.url = 'https://es.yahoo.com'
        short_url_2.user = self.user
        short_url_2.save()

        s = ShortUrlSerializer([short_url_1, short_url_2], many=True)

        url = reverse('shortener_app:api_list_urls')
        response = self.client.get(url, format='json', **self.headers)

        self.assert_response_ok(response, s.data)

    def test_url_delete_authentication_error(self):
        """
        Ensure we can create a new account object.
        """
        short_url_1 = ShortUrl()
        short_url_1.url = 'https://www.google.com'
        short_url_1.user = self.user
        short_url_1.save()
        url = reverse(
            'shortener_app:api_delete_url', kwargs={'uid': short_url_1.uid})
        self.headers = {self.header_name: 'invalid-api-key'}

        response = self.client.get(url, format='json', **self.headers)

        self.assert_authentication_failed(response)

    def test_url_delete_bad_uid(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse(
            'shortener_app:api_delete_url', kwargs={'uid': 'invalid_uid'})

        response = self.client.post(url, format='json', **self.headers)

        self.assertEqual(response.data, {'error': 'Url does not exist'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_url_delete(self):
        """
        Ensure we can create a new account object.
        """
        short_url_1 = ShortUrl()
        short_url_1.url = 'https://www.google.com'
        short_url_1.user = self.user
        short_url_1.save()
        url = reverse(
            'shortener_app:api_delete_url', kwargs={'uid': short_url_1.uid})

        response = self.client.post(url, format='json', **self.headers)

        self.assert_response_ok(response, {})
        with self.assertRaises(ShortUrl.DoesNotExist):
            ShortUrl.objects.get(id=short_url_1.id)

    def test_url_create_authentication_error(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('shortener_app:api_create_url')
        self.headers = {self.header_name: 'invalid-api-key'}

        response = self.client.get(url, format='json', **self.headers)

        self.assert_authentication_failed(response)

    def test_url_create_invalid_target_url(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('shortener_app:api_create_url')
        data = {'target': 'google'}

        response = self.client.post(
            url, data=data, format='json', **self.headers)

        short_url = ShortUrl.objects.filter(user=self.user).first()
        self.assertEqual(short_url, None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid url'})

    def test_url_create(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('shortener_app:api_create_url')
        data = {'target': 'https://google.com'}

        response = self.client.post(
            url, data=data, format='json', **self.headers)

        short_url = ShortUrl.objects.filter(user=self.user).first()
        s = ShortUrlSerializer(short_url)
        self.assertNotEqual(short_url, None)
        self.assert_response_ok(response, s.data)
