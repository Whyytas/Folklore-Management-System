from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Ensembles.models import Ensemble
from Departments.models import Department

User = get_user_model()

class EnsembleViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='adminpass', role='administratorius')
        self.member = User.objects.create_user(username='member', password='memberpass', role='narys')
        self.department = Department.objects.create(title="Padalinys A")
        self.ensemble = Ensemble.objects.create(title="Ansamblis A", city="Kaunas", department=self.department)

    def test_ensemble_list_view_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('ansambliai_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ansamblis A")

    def test_ensemble_list_view_as_member_forbidden(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('ansambliai_list'))
        self.assertEqual(response.status_code, 403)

    def test_ensemble_add_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('ansamblis_add'), {
            'title': 'Ansamblis B',
            'city': 'Vilnius',
            'department': self.department.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ensemble.objects.filter(title='Ansamblis B').exists())

    def test_ensemble_edit_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('ansamblis_edit', args=[self.ensemble.id]), {
            'title': 'Ansamblis Atnaujintas',
            'city': self.ensemble.city,
            'department': self.department.id
        })
        self.assertEqual(response.status_code, 302)
        self.ensemble.refresh_from_db()
        self.assertEqual(self.ensemble.title, 'Ansamblis Atnaujintas')

    def test_ensemble_delete_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('ansamblis_delete', args=[self.ensemble.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ensemble.objects.filter(id=self.ensemble.id).exists())

    def test_ensemble_edit_forbidden_for_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('ansamblis_edit', args=[self.ensemble.id]))
        self.assertEqual(response.status_code, 403)

    def test_ensemble_delete_forbidden_for_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.post(reverse('ansamblis_delete', args=[self.ensemble.id]))
        self.assertEqual(response.status_code, 403)
