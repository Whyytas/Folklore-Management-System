from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Ensembles.models import Ensemble
from Pieces.models import Piece
from Rehearsals.models import Rehearsal, RehearsalPiece
from django.utils.timezone import now, timedelta
import json

User = get_user_model()

class RehearsalViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='adminpass', role='administratorius')
        self.member = User.objects.create_user(username='member', password='memberpass', role='narys')
        self.ensemble = Ensemble.objects.create(title='Ansamblis A')
        self.piece1 = Piece.objects.create(title='Kūrinys 1')
        self.piece2 = Piece.objects.create(title='Kūrinys 2')

    def test_rehearsals_list_access(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('rehearsals'))
        self.assertEqual(response.status_code, 200)

    def test_rehearsal_create_post_success(self):
        self.client.login(username='admin', password='adminpass')
        data = {
            "title": "Test Rehearsal",
            "date": now().strftime('%Y-%m-%d %H:%M'),
            "pieces": [self.piece1.id, self.piece2.id],
            "ensemble": self.ensemble.id
        }
        response = self.client.post(reverse('repeticija_create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Rehearsal.objects.filter(title="Test Rehearsal").exists())

    def test_rehearsal_create_forbidden_for_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('repeticija_create'))
        self.assertEqual(response.status_code, 403)

    def test_rehearsal_edit_post_success(self):
        self.client.login(username='admin', password='adminpass')
        rehearsal = Rehearsal.objects.create(title='Old Title', date=now(), ensemble=self.ensemble)
        data = {
            "title": "New Title",
            "date": now().strftime('%Y-%m-%d %H:%M'),
            "pieces": [self.piece1.id],
            "ensemble": self.ensemble.id
        }
        response = self.client.post(reverse('repeticija_edit', args=[rehearsal.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        rehearsal.refresh_from_db()
        self.assertEqual(rehearsal.title, "New Title")

    def test_rehearsal_detail_view(self):
        rehearsal = Rehearsal.objects.create(title='Reh Detail', date=now(), ensemble=self.ensemble)
        RehearsalPiece.objects.create(rehearsal=rehearsal, piece=self.piece1, order=0)
        RehearsalPiece.objects.create(rehearsal=rehearsal, piece=self.piece2, order=1)

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('repeticija_detail', args=[rehearsal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reh Detail')

    def test_rehearsal_delete_success(self):
        self.client.login(username='admin', password='adminpass')
        rehearsal = Rehearsal.objects.create(title='ToDelete', date=now(), ensemble=self.ensemble)
        response = self.client.post(reverse('repeticija_delete', args=[rehearsal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Rehearsal.objects.filter(id=rehearsal.id).exists())
