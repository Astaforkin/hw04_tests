
from django.test import Client, TestCase
from django.urls import reverse


class AboutViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_names_exists_at_desired_locations(self):
        """Проверяем доступность страниц по app:name приложения About."""

        pages_names = [
            reverse('about:author'),
            reverse('about:tech'),
        ]

        for address in pages_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.reason_phrase, 'OK')

    def test_about_uses_correct_templates(self):
        """URL-адреса используют соответствующие шаблоны в приложении About."""

        pages_templates_names = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html'
        }

        for reverse_name, template in pages_templates_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_urls_exists_at_desired_locations(self):
        """Проверяем доступность страниц по URL приложения About."""

        url_names = [
            '/about/author/',
            '/about/tech/',
        ]

        for address in url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.reason_phrase, 'OK')

    def test_about_urls_uses_correct_template(self):
        """Проверяем шаблоны страниц приложения About."""

        url_templates_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }

        for address, template in url_templates_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
