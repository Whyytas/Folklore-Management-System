from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from unittest.mock import patch

User = get_user_model()

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='test@resend.dev'
)
class PasswordResetFlowTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@resend.dev',
            password='initialpassword'
        )

    def test_forgot_password_view_renders(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forgot_password.html')

    def test_password_reset_email_sent(self):
        with patch("Initial.forms.resend.Emails.send") as mocked_send:
            response = self.client.post(reverse('forgot_password'), {'email': 'test@resend.dev'})
            self.assertRedirects(response, reverse('password_reset_done'))
            mocked_send.assert_called_once()

    def test_password_reset_confirm_view(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        # Initial URL with the token
        initial_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

        # Step 1: Visit the initial URL which should redirect to the "set-password" URL
        response = self.client.get(initial_url, follow=True)
        self.assertEqual(response.status_code, 200)

        # Extract the redirect URL path which should contain "set-password"
        reset_url = response.request['PATH_INFO']

        # Step 2: Now post to this URL with the new password
        response = self.client.post(reset_url, {
            'new_password1': 'newsecurepassword123',
            'new_password2': 'newsecurepassword123'
        })

        # Now it should redirect to the complete page
        self.assertRedirects(response, reverse('password_reset_complete'))

        # Verify the password was actually changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newsecurepassword123'))
    def test_password_reset_complete_view(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_complete.html')