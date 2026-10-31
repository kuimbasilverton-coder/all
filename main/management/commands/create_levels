
from django.core.management.base import BaseCommand
from main.models import Level

class Command(BaseCommand):
    help = 'Create 10 default levels'

    def handle(self, *args, **options):
        titles = [
            "Introduction to AI", "History of AI", "Machine Learning Basics", "Deep Learning",
            "Natural Language Processing", "Computer Vision", "Reinforcement Learning",
            "AI Ethics", "AI Applications", "Future of AI"
        ]
        for i, title in enumerate(titles, start=1):
            level, created = Level.objects.get_or_create(number=i, defaults={'title': title})
            if created:
                self.stdout.write(f"Level {i} created: {title}")
            else:
                self.stdout.write(f"Level {i} already exists: {title}")
