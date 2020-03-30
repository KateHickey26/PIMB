from django.test import TestCase, Client, override_settings
from django.urls import reverse

# Create your tests here.

@override_settings(SECURE_SSL_REDIRECT=False)
class InspeakersTest(TestCase):

    def setUp(self):
        self.client = Client()

    # Test about page
    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed('inspeakers/about.html')

    # Test that the login page redirects to home page after logging in
    def test_redirect_after_login(self):
        response = self.client.post(reverse('inspeakers:login'), {"username": "jsmith", "password": "jsmith123"})
        self.assertRedirects(response, reverse('inspeakers:home'))


