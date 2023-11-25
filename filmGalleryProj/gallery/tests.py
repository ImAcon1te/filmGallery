from django.test import TestCase
from .models import Film, Comment, Category
import datetime
from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class FilmTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.film = Film.objects.create(
            title='Test Film',
            description='Test description',
            time_filmed=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            film_rating=4.5,
            poster_url='http://example.com/poster.jpg',
            cat=self.category,
            user=self.user
        )

    def test_film_title(self):
        self.assertEqual(self.film.title, 'Test Film')

    def test_film_description(self):
        self.assertEqual(self.film.description, 'Test description')

    def test_film_time_filmed(self):
        self.assertEqual(self.film.time_filmed, datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))

    def test_film_rating(self):
        self.assertEqual(self.film.film_rating, 4.5)

    def test_film_poster_url(self):
        self.assertEqual(self.film.poster_url, 'http://example.com/poster.jpg')

    def test_film_category(self):
        self.assertEqual(self.film.cat, self.category)

    def test_film_user(self):
        self.assertEqual(self.film.user, self.user)

class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.film = Film.objects.create(
            title='Test Film',
            description='Test description',
            time_filmed=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            film_rating=4.5,
            poster_url='http://example.com/poster.jpg',
            cat=self.category,
            user=self.user
        )
        self.comment = Comment.objects.create(
            movie=self.film,
            user=self.user,
            comment_rating=3.0,
            text='Test comment'
        )

    def test_comment_rating(self):
        self.assertEqual(self.comment.comment_rating, 3.0)

    def test_comment_text(self):
        self.assertEqual(self.comment.text, 'Test comment')

    def test_comment_movie(self):
        self.assertEqual(self.comment.movie, self.film)

    def test_comment_user(self):
        self.assertEqual(self.comment.user, self.user)

class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_name(self):
        self.assertEqual(self.category.name, 'Test Category')

class GalleryAPIUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.film = Film.objects.create(
            title='Test Film',
            description='Test description',
            time_filmed='2023-11-22 12:00:00',
            film_rating=4.5,
            poster_url='http://example.com/poster.jpg',
            cat=self.category,
            user=self.user
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_gallery_api_update(self):
        url = reverse('gallery-update', kwargs={'pk': self.film.id})
        data = {
            'title': 'Updated Film Title',
            'description': 'Updated description',
            'time_filmed': '2023-12-01 14:00:00',
            'film_rating': 3.0,
            'poster_url': 'http://example.com/new_poster.jpg'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.get(id=self.film.id).title, 'Updated Film Title')


    def test_gallery_api_update_unauthorized(self):
        self.client.force_authenticate(user=None)  # Отключение аутентификации
        url = reverse('gallery-update', kwargs={'pk': self.film.id})
        data = {
            'title': 'Updated Film Title',
            'description': 'Updated description',
            'film_rating': 3.0,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class GalleryAPIDestroyTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.film = Film.objects.create(
            title='Test Film',
            description='Test description',
            time_filmed='2023-11-22 12:00:00',
            film_rating=4.5,
            poster_url='http://example.com/poster.jpg',
            cat=self.category,
            user=self.user
        )
        self.token_admin = Token.objects.create(user=self.admin_user)
        self.token_user = Token.objects.create(user=self.user)
        self.client_admin = APIClient()
        self.client_admin.credentials(HTTP_AUTHORIZATION=f'Token {self.token_admin.key}')
        self.client_user = APIClient()
        self.client_user.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user.key}')

    def test_gallery_api_destroy_admin(self):
        url = reverse('gallery-destroy', kwargs={'pk': self.film.id})
        response = self.client_admin.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Film.objects.filter(id=self.film.id).exists())

    def test_gallery_api_destroy_user(self):
        url = reverse('gallery-destroy', kwargs={'pk': self.film.id})
        response = self.client_user.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Film.objects.filter(id=self.film.id).exists())

    def test_gallery_api_destroy_unauthenticated(self):
        self.client_user.credentials()  # Отключение аутентификации
        url = reverse('gallery-destroy', kwargs={'pk': self.film.id})
        response = self.client_user.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Film.objects.filter(id=self.film.id).exists())

class CommentAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.film = Film.objects.create(
            title='Test Film',
            description='Test description',
            time_filmed='2023-11-22 12:00:00',
            film_rating=4.5,
            poster_url='http://example.com/poster.jpg',
            cat=self.category,
            user=self.user
        )
        self.comment = Comment.objects.create(
            movie=self.film,
            user=self.user,
            comment_rating=4.0,
            text='Test Comment'
        )
        self.token_admin = Token.objects.create(user=self.admin_user)
        self.token_user = Token.objects.create(user=self.user)
        self.client_admin = APIClient()
        self.client_admin.credentials(HTTP_AUTHORIZATION=f'Token {self.token_admin.key}')
        self.client_user = APIClient()
        self.client_user.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user.key}')

    def test_comment_api_list(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_api_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user.key}')
        url = reverse('comment-list')
        data = {
            'movie': self.film.id,
            'user': self.user.id,
            'comment_rating': 4.5,
            'text': 'New Comment'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_api_update_not_owner(self):
        url = reverse('comment-update', kwargs={'pk': self.comment.id})
        data = {
            'comment_rating': 3.0,
            'text': 'Updated Comment'
        }
        response = self.client_admin.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_api_destroy_admin(self):
        url = reverse('comment-destroy', kwargs={'pk': self.comment.id})
        response = self.client_admin.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_comment_api_destroy_user(self):
        url = reverse('comment-destroy', kwargs={'pk': self.comment.id})
        response = self.client_user.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

    def test_comment_api_destroy_unauthenticated(self):
        self.client_user.credentials()  # Отключение аутентификации
        url = reverse('comment-destroy', kwargs={'pk': self.comment.id})
        response = self.client_user.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())