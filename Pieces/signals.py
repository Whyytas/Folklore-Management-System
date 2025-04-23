from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from .models import Piece
from Ensembles.models import Ensemble

@receiver(post_delete, sender=Ensemble)
def delete_orphan_kuriniai(sender, instance, **kwargs):
    kuriniai = Piece.objects.filter(ensembles=instance)
    for k in kuriniai:
        if k.ensembles.count() == 0:
            k.delete()
