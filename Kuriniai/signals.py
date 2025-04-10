from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from .models import Kurinys
from Ansambliai.models import Ansamblis

@receiver(post_delete, sender=Ansamblis)
def delete_orphan_kuriniai(sender, instance, **kwargs):
    kuriniai = Kurinys.objects.filter(ansambliai=instance)
    for k in kuriniai:
        if k.ansambliai.count() == 0:
            k.delete()
