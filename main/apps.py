from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # Don't import main.signals - your signals are in models.py
        # which Django already loads. Just register the subject creator here.
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver

        @receiver(post_migrate)
        def create_subjects(sender, **kwargs):
            # Only run for THIS app
            if sender.name != 'main':
                return
            from .models import Subject, SUBJECT_CHOICES
            for name, _ in SUBJECT_CHOICES:
                Subject.objects.get_or_create(name=name)
