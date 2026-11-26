from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

def create_subjects(sender, **kwargs):
    # Only run for main app, not for auth, admin, etc.
    if sender.name != 'main':
        return
    from .models import Subject, SUBJECT_CHOICES
    for name, _ in SUBJECT_CHOICES:
        Subject.objects.get_or_create(name=name)

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # Connect with weak=False so Python doesn't delete it
        post_migrate.connect(create_subjects, weak=False)
