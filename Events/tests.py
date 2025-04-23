from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from Ensembles.models import Ensemble
from Events.models import Event
from Programs.models import Program

User = get_user_model()

class EventViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='adminpass', role='administratorius')
        self.member = User.objects.create_user(username='member', password='memberpass', role='narys')
        self.ensemble = Ensemble.objects.create(title='Ansamblis X')
        self.program = Program.objects.create(title="Programa A", type="Vakaronei", ensemble=self.ensemble)
        self.event = Event.objects.create(
            title='Renginys A',
            address='Adresas 123',
            date=now() + timedelta(days=1),
            ensemble=self.ensemble,
            program=self.program
        )

    def test_event_list_view_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('renginiai'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Renginys A')

    def test_event_add_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('renginiai_add'), {
            'title': 'Renginys B',
            'address': 'Adresas 456',
            'date': (now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M'),
            'ensemble': self.ensemble.id,
            'program': self.program.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='Renginys B').exists())

    def test_event_add_forbidden_for_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('renginiai_add'))
        self.assertEqual(response.status_code, 403)

    def test_event_edit_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('renginiai_edit', args=[self.event.id]), {
            'title': 'Renginys Atnaujintas',
            'address': self.event.address,
            'date': self.event.date.strftime('%Y-%m-%d %H:%M'),
            'ensemble': self.ensemble.id,
            'program': self.program.id
        })
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Renginys Atnaujintas')

    def test_event_edit_forbidden_for_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('renginiai_edit', args=[self.event.id]))
        self.assertEqual(response.status_code, 403)

    def test_event_delete_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('renginiai_delete', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_event_delete_forbidden_for_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.post(reverse('renginiai_delete', args=[self.event.id]))
        self.assertEqual(response.status_code, 403)
