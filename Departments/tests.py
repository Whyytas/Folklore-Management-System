from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Departments.models import Department

User = get_user_model()

class DepartmentViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='adminpass', role='administratorius')
        self.department = Department.objects.create(
            title='Kultūros centras',
            address='Vilniaus g. 1',
            phone='+37060000000'
        )

    def test_departments_list_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('padaliniai_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kultūros centras')

    def test_department_add(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('padaliniai_add'), {
            'title': 'Naujas padalinys',
            'address': 'Gedimino pr. 10',
            'phone': '+37061234567'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Department.objects.filter(title='Naujas padalinys').exists())

    def test_department_edit(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('padaliniai_edit', args=[self.department.id]), {
            'title': 'Atnaujintas padalinys',
            'address': self.department.address,
            'phone': self.department.phone
        })
        self.assertEqual(response.status_code, 302)
        self.department.refresh_from_db()
        self.assertEqual(self.department.title, 'Atnaujintas padalinys')

    def test_department_delete(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('padaliniai_delete', args=[self.department.id]))
        self.assertRedirects(response, reverse('padaliniai_list'))
        self.assertFalse(Department.objects.filter(id=self.department.id).exists())