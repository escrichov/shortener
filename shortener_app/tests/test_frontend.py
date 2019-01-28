from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from shortener_app.models import ShortUrl, ShortUrlLog


class FrontendTestCase(TestCase):

    def test_index(self):
        response = self.client.get(reverse('shortener_app:index'))

        self.assertTemplateUsed(response, 'shortener_app/index.html')
        self.assertEquals(response.status_code, 200)

    def test_pricing(self):
        response = self.client.get(reverse('shortener_app:pricing'))

        self.assertTemplateUsed(response, 'shortener_app/pricing.html')
        self.assertEquals(response.status_code, 200)

    def test_info_short_url_not_exist(self):
        response = self.client.get(
            reverse('shortener_app:info', kwargs={'short_url_uid': '123456'}))

        self.assertEqual(response.content, b'Not found')
        self.assertEqual(response.status_code, 404)

    def test_info_url_of_other_user(self):
        user = get_user_model().objects.create_user(
            email='edith@hispage.com', password='fdfasd890')

        short_url = ShortUrl()
        short_url.user = user
        short_url.url = 'https://google.com'
        short_url.save()

        response = self.client.get(
            reverse(
                'shortener_app:info', kwargs={'short_url_uid': short_url.uid}))

        self.assertEqual(response.content, b'Not found')
        self.assertEqual(response.status_code, 404)

    def test_info(self):
        short_url = ShortUrl()
        short_url.url = 'https://google.com'
        short_url.save()

        response = self.client.get(
            reverse(
                'shortener_app:info', kwargs={'short_url_uid': short_url.uid}))

        self.assertTemplateUsed(response, 'shortener_app/info.html')
        self.assertEquals(response.status_code, 200)

    def test_shorten_no_url_provided(self):
        response = self.client.post(reverse('shortener_app:shorten'))

        self.assertEqual(response.content, b'No url provided')
        self.assertEqual(response.status_code, 404)

    def test_shorten_invalid_url(self):
        response = self.client.post(
            reverse('shortener_app:shorten'), data={'url': 'https://google'})

        self.assertEqual(response.content, b'Invalid url')
        self.assertEqual(response.status_code, 404)

    def test_shorten_logged_in(self):
        user = get_user_model().objects.create_user(
            email='edith@hispage.com', password='fdfasd890')
        self.client.login(email=user.email, password='fdfasd890')

        response = self.client.post(
            reverse('shortener_app:shorten'),
            data={'url': 'https://google.com'})

        short_url = ShortUrl.objects.first()
        self.assertNotEqual(short_url, None)
        self.assertEqual(short_url.user, user)
        self.assertRedirects(response, reverse('shortener_app:urls'))

    def test_shorten(self):
        response = self.client.post(
            reverse('shortener_app:shorten'),
            data={'url': 'https://google.com'})

        short_url = ShortUrl.objects.first()
        self.assertNotEqual(short_url, None)
        self.assertEqual(short_url.user, None)
        self.assertRedirects(
            response,
            reverse(
                'shortener_app:info', kwargs={'short_url_uid': short_url.uid}))

    def test_url_redirect(self):
        short_url = ShortUrl()
        short_url.clicks = 2
        short_url.user = None
        short_url.url = 'https://google.com'
        short_url.save()

        response = self.client.get(
            reverse(
                'shortener_app:url_redirect',
                kwargs={'short_url_uid': short_url.uid}))

        short_url = ShortUrl.objects.first()
        self.assertNotEqual(short_url, None)
        self.assertEqual(short_url.clicks, 3)
        self.assertRedirects(
            response, 'https://google.com', fetch_redirect_response=False)

    def test_url_redirect_log_created(self):
        short_url = ShortUrl()
        short_url.url = 'https://google.com'
        short_url.save()
        url = reverse(
            'shortener_app:url_redirect',
            kwargs={'short_url_uid': short_url.uid})
        headers = {
            'HTTP_REFERER':
            'google.com',
            'HTTP_USER_AGENT':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        }

        self.client.get(url, **headers)

        short_url = ShortUrl.objects.first()
        log = ShortUrlLog.objects.first()
        self.assertEqual(log.ip, '127.0.0.1')
        self.assertEqual(log.referer, headers.get('HTTP_REFERER'))
        self.assertEqual(log.user_agent, headers.get('HTTP_USER_AGENT'))
        self.assertEqual(log.os, 'Linux')
        self.assertEqual(log.browser, 'Chrome')
        self.assertEqual(log.country_code, None)
        self.assertEqual(log.latitude, None)
        self.assertEqual(log.longitude, None)
        self.assertEqual(log.short_url, short_url)

    def test_url_redirect_short_url_not_exist(self):
        response = self.client.get(
            reverse(
                'shortener_app:url_redirect',
                kwargs={'short_url_uid': '123456'}))

        self.assertEqual(response.content, b'Not found')
        self.assertEqual(response.status_code, 404)
