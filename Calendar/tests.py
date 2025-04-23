from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from Ensembles.models import Ensemble
from Events.models import Event
from Rehearsals.models import Rehearsal

User = get_user_model()

class CalendarViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.ensemble = Ensemble.objects.create(title="Ansamblis Test", city="Vilnius")
        self.user = User.objects.create_user(username="admin", password="adminpass", role="administratorius")
        self.client.login(username="admin", password="adminpass")
        self.session = self.client.session
        self.session["selected_ensemble_id"] = self.ensemble.id
        self.session.save()

        self.event = Event.objects.create(
            title="Test Event",
            address="Test Street",
            date=now() + timedelta(days=1),
            ensemble=self.ensemble
        )

        self.rehearsal = Rehearsal.objects.create(
            title="Test Rehearsal",
            date=now() + timedelta(days=2),
            ensemble=self.ensemble
        )

    def test_calendar_view_status(self):
        response = self.client.get(reverse("kalendorius"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ansamblis Test")

    def test_calendar_events_json(self):
        response = self.client.get(reverse("kalendorius_events"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()
        self.assertTrue(any(e["title"] == "Test Event" for e in data))
        self.assertTrue(any(e["title"] == "Test Rehearsal" for e in data))
        self.assertTrue(all("start" in e and "url" in e for e in data))
