from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
import resend

class NoEmailPasswordResetForm(PasswordResetForm):
    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            html_content = f"""
            Sveiki {user.get_username()},<br><br>
            Norėdami atstatyti slaptažodį, spauskite žemiau esantį mygtuką:<br><br>
            <a href="{reset_link}" style="padding:10px 20px;background:#17a2b8;color:white;border-radius:5px;text-decoration:none;">Atkurti slaptažodį</a><br><br>
            Jei tai nebuvote jūs – ignoruokite šį laišką.
            """

            try:
                resend.Emails.send({
                    "from": settings.DEFAULT_FROM_EMAIL,
                    "to": [user.email],
                    "subject": "Slaptažodžio atstatymas",
                    "html": html_content,
                })
            except Exception as e:
                print(f"[Resend Error] {e}")
