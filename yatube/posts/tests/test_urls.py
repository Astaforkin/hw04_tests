from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.user_not_authorized = User.objects.create_user(
            username='test_user_not_authorized'
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост тестового пользователя в тестовой группе',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client_not_authorized = Client()
        self.authorized_client.force_login(PostsURLTests.user)
        self.authorized_client_not_authorized.force_login(
            PostsURLTests.user_not_authorized
        )

    def test_urls_exists_at_desired_location(self):
        """Проверяем доступность страниц приложения Posts."""
        templates_url_names = [
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user.username}/',
            f'/posts/{self.post.pk}/',
        ]

        for address in templates_url_names:
            with self.subTest(address=address):
                guest_response = self.guest_client.get(address, follow=True)
                authorized_response = self.authorized_client.get(address)

                self.assertEqual(guest_response.reason_phrase, 'OK')
                self.assertEqual(authorized_response.reason_phrase, 'OK')

    def test_post_edit_url_exists_at_desired_location(self):
        ("""Проверяем доступность страницы редактирования поста """
         """приложения Posts.""")
        address = f'/posts/{self.post.pk}/edit/'
        guest_response = self.guest_client.get(address, follow=True)
        authorized_response = self.authorized_client.get(address)
        authorized_not_authorized_response = (
            self.authorized_client_not_authorized.get(address)
        )

        self.assertRedirects(
            guest_response,
            f'/auth/login/?next=/posts/{self.post.pk}/edit/'
        )
        self.assertEqual(authorized_response.reason_phrase, 'OK')
        self.assertEqual(
            authorized_not_authorized_response.url,
            f'/posts/{self.post.pk}/'
        )

    def test_create_post_url_exists_at_desired_location(self):
        """
        Проверяем доступность страницы создания поста
        приложения Posts.
        """
        address = '/create/'
        guest_response = self.guest_client.get(address, follow=True)
        authorized_response = self.authorized_client.get(address)

        self.assertRedirects(
            guest_response,
            "/auth/login/?next=/create/"
        )
        self.assertEqual(authorized_response.reason_phrase, 'OK')

    def test_404_error_return_for_unexisting_page(self):
        """Проверка несуществующей страницы"""
        guest_response = self.guest_client.get(
            '/unexisting_page/', follow=True
        )
        authorized_response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(guest_response.reason_phrase, 'Not Found')
        self.assertEqual(authorized_response.reason_phrase, 'Not Found')

    def test_urls_uses_correct_template(self):
        """Проверяем шаблоны приложения Posts."""
        url_templates_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in url_templates_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
