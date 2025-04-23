from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now, timedelta
from Ensembles.models import Ensemble
from Events.models import Event
from Rehearsals.models import Rehearsal
from Pieces.models import Piece
from Instruments.models import Instrument
from django.contrib.auth import get_user_model

User = get_user_model()

class MainPageViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.ensemble = Ensemble.objects.create(title='Ansamblis A')
        self.event = Event.objects.create(title='Renginys', date=now() + timedelta(days=1), ensemble=self.ensemble)
        self.rehearsal = Rehearsal.objects.create(title='Repeticija', date=now() + timedelta(days=2), ensemble=self.ensemble)
        self.instrument = Instrument.objects.create(title='Kanklės', ensemble=self.ensemble)
        self.piece = Piece.objects.create(title='Kūrinys 1', type='Daina')
        self.piece.ensembles.add(self.ensemble)

    def test_main_page_view_success(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Renginys')
        self.assertContains(response, 'Repeticija')
        self.assertContains(response, 'Kanklės')
        self.assertContains(response, 'Kūrinys 1')

    def test_main_page_filtered_by_ensemble(self):
        ensemble_b = Ensemble.objects.create(title='Ansamblis B')
        response = self.client.get(reverse('main') + f'?ensemble_id={ensemble_b.id}')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Renginys')
        self.assertNotContains(response, 'Repeticija')

    def test_set_selected_ensemble_saves_to_session(self):
        response = self.client.get(reverse('set_selected_ansamblis'), {'ensemble_id': self.ensemble.id})
        self.assertEqual(response.status_code, 302)
        self.assertIn('selected_ensemble_id', self.client.session)
        self.assertEqual(int(self.client.session['selected_ensemble_id']), self.ensemble.id)

    def test_set_selected_ensemble_redirects_to_referer(self):
        response = self.client.get(
            reverse('set_selected_ansamblis'),
            {'ensemble_id': self.ensemble.id},
            HTTP_REFERER='/somewhere/'
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/somewhere/')
