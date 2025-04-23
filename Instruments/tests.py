from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Ensembles.models import Ensemble
from Instruments.models import Instrument
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image
import tempfile

User = get_user_model()

class InstrumentViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='adminpass', role='administratorius')
        self.member = User.objects.create_user(username='member', password='memberpass', role='narys')
        self.ensemble = Ensemble.objects.create(title='Ansamblis A')
        self.instrument = Instrument.objects.create(title='Birbynė', ensemble=self.ensemble)

    def generate_test_image(self):
        temp = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new('RGB', (100, 100))
        image.save(temp, format='JPEG')
        temp.seek(0)
        return SimpleUploadedFile(temp.name, temp.read(), content_type="image/jpeg")

    def test_instruments_list_view_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('instrumentai_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Birbynė')

    def test_instruments_list_view_as_member_forbidden(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('instrumentai_list'))
        self.assertEqual(response.status_code, 403)

    def test_instrument_add_success(self):
        self.client.login(username='admin', password='adminpass')
        photo = self.generate_test_image()
        response = self.client.post(reverse('instrumentai_add'), {
            'title': 'Kanklės',
            'photo': photo,
            'ensemble': self.ensemble.id
        })

        if response.status_code == 200 and hasattr(response, 'context') and response.context:
            print("Form errors:", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Instrument.objects.filter(title='Kanklės').exists())

    def test_instrument_add_forbidden_for_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.get(reverse('instrumentai_add'))
        self.assertEqual(response.status_code, 403)

    def test_instrument_edit_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('instrumentai_edit', args=[self.instrument.id]), {
            'title': 'Atnaujinta Birbynė',
            'ensemble': self.ensemble.id
        })
        self.assertEqual(response.status_code, 302)
        self.instrument.refresh_from_db()
        self.assertEqual(self.instrument.title, 'Atnaujinta Birbynė')

    def test_instrument_delete_success(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('instrumentai_delete', args=[self.instrument.id]))
        self.assertRedirects(response, reverse('instrumentai_list'))
        self.assertFalse(Instrument.objects.filter(id=self.instrument.id).exists())