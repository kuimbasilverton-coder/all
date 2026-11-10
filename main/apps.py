from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals  # Adjust if your app name differs

        # Create subjects AFTER migrations finish - no more warning
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver

        @receiver(post_migrate, sender=self)
        def create_subjects(sender, **kwargs):
            from .models import Subject, SUBJECT_CHOICES
            for name, _ in SUBJECT_CHOICES:
                Subject.objects.get_or_create(name=name)
