from django.db.models.signals import post_save  # signalas post_save
from django.contrib.auth.models import User  # django useriu klase
from django.dispatch import receiver  # signalo gavejas
from .models import Profilis

# Sukurus vartotoja automatiskai sukuriamas profilis
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profilis.objects.create(user=instance)

# Issaugoti korekcijas vartotojo (pvz.password)
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profilis.save()