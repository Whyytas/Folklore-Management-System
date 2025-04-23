from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Ensembles.models import Ensemble
from Pieces.models import Piece
from Programs.models import Program, ProgramPiece
import json

User = get_user_model()

class ProgramViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='adminpass', role='administratorius')
        self.member = User.objects.create_user(username='member', password='memberpass', role='narys')
        self.ensemble = Ensemble.objects.create(title='Ensemble A')
        self.piece = Piece.objects.create(title='Piece 1', duration='03:00', type='Daina')

    def test_programs_list_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('programos'))
        self.assertEqual(response.status_code, 200)

    def test_program_create_success(self):
        self.client.login(username='admin', password='adminpass')
        data = {
            "title": "Program 1",
            "type": "Adventui",
            "description": "Test",
            "ensemble": self.ensemble.id,
            "pieces": [{"id": self.piece.id, "queue": 0}]
        }
        response = self.client.post(reverse('program_create'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Program.objects.filter(title='Program 1').exists())

    def test_program_create_forbidden_for_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('program_create'))
        self.assertEqual(response.status_code, 403)

    def test_program_edit_success(self):
        self.client.login(username='admin', password='adminpass')
        program = Program.objects.create(title='Old', type='Adventui', ensemble=self.ensemble)
        data = {
            "title": "New",
            "type": "Adventui",
            "description": "Updated",
            "duration": "05:00",
            "ensemble": self.ensemble.id,
            "pieces": [{"id": self.piece.id, "queue": 1}]
        }
        response = self.client.post(reverse('program_edit', args=[program.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        program.refresh_from_db()
        self.assertEqual(program.title, "New")
        self.assertEqual(program.duration, "05:00")

    def test_program_delete_success(self):
        self.client.login(username='admin', password='adminpass')
        program = Program.objects.create(title='ToDelete', type='Adventui', ensemble=self.ensemble)
        response = self.client.post(reverse('program_delete', args=[program.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Program.objects.filter(id=program.id).exists())

    def test_programs_pieces_view(self):
        self.client.login(username='admin', password='adminpass')
        program = Program.objects.create(title='Test View', type='Adventui', ensemble=self.ensemble)
        ProgramPiece.objects.create(program=program, piece=self.piece, queue=0)
        response = self.client.get(reverse('programos_kuriniai', args=[program.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Piece 1')
