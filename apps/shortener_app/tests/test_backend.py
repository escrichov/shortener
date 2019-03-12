from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from shortener_app.models import ShortUrl, APIAccess
from payments.models import Subscription


class BackendTestNotLoggedInCase(TestCase):

    def login_redirect_url(self, url):
        return settings.LOGIN_URL + '?next={url}'.format(url=url)

    def test_profile_no_logged_in(self):
        url = reverse('shortener_app:profile')
        response = self.client.get(url)

        self.assertRedirects(response, self.login_redirect_url(url))

    def test_list_urls_no_logged_in(self):
        url = reverse('shortener_app:urls')
        response = self.client.get(url)

        self.assertRedirects(response, self.login_redirect_url(url))

    def test_delete_no_logged_in(self):
        url = reverse(
            'shortener_app:delete', kwargs={'short_url_uid': '123456'})
        response = self.client.get(url)

        self.assertRedirects(response, self.login_redirect_url(url))

    def test_stats_no_logged_in(self):
        url = reverse('shortener_app:stats', kwargs={'short_url_uid': '123456'})
        response = self.client.get(url)

        self.assertRedirects(response, self.login_redirect_url(url))

    def test_create_api_access_logged_in(self):
        url = reverse('shortener_app:create_api_access')
        response = self.client.get(url)

        self.assertRedirects(response, self.login_redirect_url(url))

    def test_delete_api_access_no_logged_in(self):
        url = reverse(
            'shortener_app:delete_api_access', kwargs={'api_access_id': 1})
        response = self.client.get(url)

        self.assertRedirects(response, self.login_redirect_url(url))


class BackendTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user( # nosec
            email='edith@hispage.com', password='fdfasd890')
        self.client.login( # nosec
            email=self.user.email, password='fdfasd890')

    def test_profile(self):
        response = self.client.get(reverse('shortener_app:profile'))

        self.assertTemplateUsed(response, 'shortener_app/profile.html')
        self.assertEquals(response.status_code, 200)

    def test_profile_api_access(self):
        api_access = APIAccess()
        api_access.user = self.user
        api_access.save()

        response = self.client.get(reverse('shortener_app:profile'))

        self.assertTemplateUsed(response, 'shortener_app/profile.html')
        self.assertContains(response, api_access.apikey)
        self.assertEquals(response.status_code, 200)

    def test_profile_active_subscription(self):
        subscription = Subscription()
        subscription.user = self.user
        subscription.state = Subscription.STATE_ACTIVE
        subscription.save()

        response = self.client.get(reverse('shortener_app:profile'))

        self.assertTemplateUsed(response, 'shortener_app/profile.html')
        self.assertContains(response, "You have premium account plan")
        self.assertEquals(response.status_code, 200)

    def test_profile_no_active_subscription(self):
        subscription = Subscription()
        subscription.user = self.user
        subscription.state = Subscription.STATE_CANCELLED
        subscription.save()

        response = self.client.get(reverse('shortener_app:profile'))

        self.assertTemplateUsed(response, 'shortener_app/profile.html')
        self.assertContains(response, "1€/Month")
        self.assertEquals(response.status_code, 200)

    def test_list_urls_empty_list(self):
        response = self.client.get(reverse('shortener_app:urls'))

        self.assertTemplateUsed(response, 'shortener_app/list_urls.html')
        self.assertEquals(response.status_code, 200)

    def test_list_urls(self):
        short_url = ShortUrl()
        short_url.user = self.user
        short_url.url = 'https://google.com'
        short_url.save()

        response = self.client.get(reverse('shortener_app:urls'))

        self.assertTemplateUsed(response, 'shortener_app/list_urls.html')
        self.assertContains(response, short_url.url)
        self.assertEquals(response.status_code, 200)

    def test_upgrade_to_premium_user_has_no_subscription(self):
        response = self.client.get(reverse('shortener_app:upgrade_to_premium'))

        self.assertTemplateUsed(response,
                                'shortener_app/upgrade_to_premium.html')
        self.assertContains(response, "Price")
        self.assertEquals(response.status_code, 200)

    def test_upgrade_to_premium_user_has_cancelled_subscription(self):
        subscription = Subscription()
        subscription.user = self.user
        subscription.state = Subscription.STATE_CANCELLED
        subscription.save()

        response = self.client.get(reverse('shortener_app:upgrade_to_premium'))

        self.assertTemplateUsed(response,
                                'shortener_app/upgrade_to_premium.html')
        self.assertContains(response, "Price")
        self.assertEquals(response.status_code, 200)

    def test_upgrade_to_premium_user_has_active_subscription(self):
        subscription = Subscription()
        subscription.user = self.user
        subscription.state = Subscription.STATE_ACTIVE
        subscription.save()

        response = self.client.get(reverse('shortener_app:upgrade_to_premium'))

        self.assertTemplateUsed(response,
                                'shortener_app/upgrade_to_premium.html')
        self.assertContains(response, "You have premium account plan")
        self.assertEquals(response.status_code, 200)

    def test_delete(self):
        short_url = ShortUrl()
        short_url.user = self.user
        short_url.url = 'https://google.com'
        short_url.save()

        response = self.client.get(
            reverse(
                'shortener_app:delete', kwargs={'short_url_uid':
                                                short_url.uid}))

        with self.assertRaises(ShortUrl.DoesNotExist):
            ShortUrl.objects.get(id=short_url.id)
        self.assertRedirects(response, reverse('shortener_app:urls'))

    def test_delete_short_url_not_exist(self):
        response = self.client.get(
            reverse('shortener_app:delete', kwargs={'short_url_uid': '123456'}))

        self.assertRedirects(response, reverse('shortener_app:urls'))

    def test_stats(self):
        short_url = ShortUrl()
        short_url.user = self.user
        short_url.url = 'https://google.com'
        short_url.save()

        response = self.client.get(
            reverse(
                'shortener_app:stats', kwargs={'short_url_uid': short_url.uid}))

        self.assertTemplateUsed(response, 'shortener_app/stats.html')
        self.assertEquals(response.status_code, 200)

    def test_stats_short_url_not_exist(self):
        response = self.client.get(
            reverse('shortener_app:stats', kwargs={'short_url_uid': '123456'}))

        self.assertEqual(response.content, b'Not found')
        self.assertEqual(response.status_code, 404)

    def test_create_api_access(self):
        response = self.client.get(reverse('shortener_app:create_api_access'))

        api_access = APIAccess.objects.first()
        self.assertEqual(api_access.user, self.user)
        self.assertRedirects(response, reverse('shortener_app:profile'))

    def test_delete_api_access(self):
        api_access = APIAccess()
        api_access.user = self.user
        api_access.save()

        response = self.client.get(
            reverse(
                'shortener_app:delete_api_access',
                kwargs={'api_access_id': api_access.id}))

        self.assertEqual(api_access.user, self.user)
        self.assertRedirects(response, reverse('shortener_app:profile'))

    def test_delete_api_access_not_exist(self):
        response = self.client.get(
            reverse(
                'shortener_app:delete_api_access', kwargs={'api_access_id': 1}))

        self.assertRedirects(response, reverse('shortener_app:profile'))
