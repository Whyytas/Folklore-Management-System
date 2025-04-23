from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Ensembles.models import Ensemble

User = get_user_model()


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='adminpass', role='administratorius')
        self.vadovas = User.objects.create_user(username='leader', password='leaderpass', role='vadovas')
        self.member = User.objects.create_user(username='member', password='memberpass', role='narys')

        self.ensemble = Ensemble.objects.create(title="Choras")
        self.vadovas.ensembles.add(self.ensemble)

    def test_users_list_access_control(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('nariai'))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='leader', password='leaderpass')
        response = self.client.get(reverse('nariai'))
        self.assertEqual(response.status_code, 200)

    def test_user_add_view_post_valid(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('nariai_add'), {
            'username': 'newuser',
            'name': 'Jonas',
            'surname': 'Jonaitis',
            'email': 'jonas@example.com',
            'phone_number': '123456789',
            'role': 'narys',
            'password1': 'VeryStrongPassword123',
            'password2': 'VeryStrongPassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_users_view_access(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('nariai_view', args=[self.vadovas.id]))
        self.assertEqual(response.status_code, 200)

        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('nariai_view', args=[self.vadovas.id]))
        self.assertEqual(response.status_code, 403)

    def test_user_edit_password_change(self):
        self.client.login(username='admin', password='adminpass')
        new_pass = 'NewSecurePass123'
        response = self.client.post(reverse('nariai_edit', args=[self.member.id]), {
            'which_form': 'password',
            'new_password1': new_pass,
            'new_password2': new_pass
        })
        self.assertEqual(response.status_code, 302)
        self.member.refresh_from_db()
        self.assertTrue(self.member.check_password(new_pass))

    def test_check_username_api(self):
        response = self.client.get(reverse('check_username') + '?username=admin')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['exists'])

        response = self.client.get(reverse('check_username') + '?username=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['exists'])

    def test_user_delete_access_control(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.post(reverse('nariai_delete', args=[self.vadovas.id]))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('nariai_delete', args=[self.vadovas.id]))
        self.assertRedirects(response, reverse('nariai'))
        self.assertFalse(User.objects.filter(id=self.vadovas.id).exists())
