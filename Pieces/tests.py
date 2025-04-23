from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from Ensembles.models import Ensemble
from Pieces.models import Piece, Feature
import io

User = get_user_model()

class PieceViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='adminpass', role='administratorius')
        self.member = User.objects.create_user(username='member', password='memberpass', role='narys')
        self.ensemble = Ensemble.objects.create(title='Ansamblis X')
        self.feature = Feature.objects.create(title='Pradžia')
        self.piece = Piece.objects.create(title='Sample Piece', type='Daina')
        self.piece.duration = "01:00"
        self.piece.ensembles.add(self.ensemble)
        self.piece.save()

    def test_pieces_list_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('pieces'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Piece')

    def test_piece_add_forbidden_for_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('pieces_add'))
        self.assertEqual(response.status_code, 403)

    def test_piece_add_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('pieces_add'), {
            "title": "New Piece",
            "type": "Daina",
            "duration": "03:15",
            "preparation": "Paruoštas",
            "ensembles": [self.ensemble.id],
            "features": [self.feature.id],
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Piece.objects.filter(title='New Piece').exists())

    def test_piece_edit_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('pieces_edit', args=[self.piece.id]), {
            "title": "Updated Piece",
            "type": "Daina",
            "duration": "02:00",
            "preparation": "Paruoštas",
            "ensembles": [self.ensemble.id],
            "features": [self.feature.id],
        })

        self.piece.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.piece.refresh_from_db()
        self.assertEqual(self.piece.title, 'Updated Piece')

    def test_piece_delete_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('pieces_delete', args=[self.piece.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Piece.objects.filter(id=self.piece.id).exists())

    def test_piece_details_api(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('piece_details', args=[self.piece.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('pavadinimas', response.json())

    def test_pieces_by_ensemble_feature(self):
        self.piece.features.add(self.feature)
        response = self.client.get(reverse('pieces_by_ensemble_feature'), {
            'ensemble': self.ensemble.id,
            'feature': self.feature.title
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(x['title'] == self.piece.title for x in response.json()))
