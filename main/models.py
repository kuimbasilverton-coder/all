from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_premium = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # added field for profile pics
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Only run when a User is CREATED. Never touch it on update/delete.
    if created:
        UserProfile.objects.create(user=instance)

class Visit(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, blank=True)
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit by {self.user or self.session_key} at {self.visit_time}"

class PasswordGate(models.Model):
    password1 = models.CharField(max_length=128, default='123')
    password2 = models.CharField(max_length=128, default='456')
    password3 = models.CharField(max_length=128, default='789')

    def __str__(self):
        return "Password Gate Config"

class FormGroup(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f'Form {self.number}'

# --- HARD-CODED SUBJECTS - PAPER 1 + PAPER 2 + PAPER 3 FOR ALL ---
SUBJECT_CHOICES = [
    # Mathematics
    ('Mathematics PAPER 1', 'Mathematics PAPER 1'),
    ('Mathematics PAPER 2', 'Mathematics PAPER 2'),
    ('Mathematics PAPER 3', 'Mathematics PAPER 3'),
    # English
    ('English PAPER 1', 'English PAPER 1'),
    ('English PAPER 2', 'English PAPER 2'),
    ('English PAPER 3', 'English PAPER 3'),
    # Shona
    ('Shona PAPER 1', 'Shona PAPER 1'),
    ('Shona PAPER 2', 'Shona PAPER 2'),
    ('Shona PAPER 3', 'Shona PAPER 3'),
    # Ndebele
    ('Ndebele PAPER 1', 'Ndebele PAPER 1'),
    ('Ndebele PAPER 2', 'Ndebele PAPER 2'),
    ('Ndebele PAPER 3', 'Ndebele PAPER 3'),
    # Science
    ('Science PAPER 1', 'Science PAPER 1'),
    ('Science PAPER 2', 'Science PAPER 2'),
    ('Science PAPER 3', 'Science PAPER 3'),
    # Combined Science
    ('Combined Science PAPER 1', 'Combined Science PAPER 1'),
    ('Combined Science PAPER 2', 'Combined Science PAPER 2'),
    ('Combined Science PAPER 3', 'Combined Science PAPER 3'),
    # Geography
    ('Geography PAPER 1', 'Geography PAPER 1'),
    ('Geography PAPER 2', 'Geography PAPER 2'),
    ('Geography PAPER 3', 'Geography PAPER 3'),
    # History
    ('History PAPER 1', 'History PAPER 1'),
    ('History PAPER 2', 'History PAPER 2'),
    ('History PAPER 3', 'History PAPER 3'),
    # Biology
    ('Biology PAPER 1', 'Biology PAPER 1'),
    ('Biology PAPER 2', 'Biology PAPER 2'),
    ('Biology PAPER 3', 'Biology PAPER 3'),
    # Physics
    ('Physics PAPER 1', 'Physics PAPER 1'),
    ('Physics PAPER 2', 'Physics PAPER 2'),
    ('Physics PAPER 3', 'Physics PAPER 3'),
    # Chemistry
    ('Chemistry PAPER 1', 'Chemistry PAPER 1'),
    ('Chemistry PAPER 2', 'Chemistry PAPER 2'),
    ('Chemistry PAPER 3', 'Chemistry PAPER 3'),
    # Accounts
    ('Accounts PAPER 1', 'Accounts PAPER 1'),
    ('Accounts PAPER 2', 'Accounts PAPER 2'),
    ('Accounts PAPER 3', 'Accounts PAPER 3'),
    # Commerce
    ('Commerce PAPER 1', 'Commerce PAPER 1'),
    ('Commerce PAPER 2', 'Commerce PAPER 2'),
    ('Commerce PAPER 3', 'Commerce PAPER 3'),
    # Computer Science
    ('Computer Science PAPER 1', 'Computer Science PAPER 1'),
    ('Computer Science PAPER 2', 'Computer Science PAPER 2'),
    ('Computer Science PAPER 3', 'Computer Science PAPER 3'),
    # Agriculture
    ('Agriculture PAPER 1', 'Agriculture PAPER 1'),
    ('Agriculture PAPER 2', 'Agriculture PAPER 2'),
    ('Agriculture PAPER 3', 'Agriculture PAPER 3'),
    # Business Studies
    ('Business Studies PAPER 1', 'Business Studies PAPER 1'),
    ('Business Studies PAPER 2', 'Business Studies PAPER 2'),
    ('Business Studies PAPER 3', 'Business Studies PAPER 3'),
    # Economics
    ('Economics PAPER 1', 'Economics PAPER 1'),
    ('Economics PAPER 2', 'Economics PAPER 2'),
    ('Economics PAPER 3', 'Economics PAPER 3'),
    # Literature
    ('Literature in English PAPER 1', 'Literature in English PAPER 1'),
    ('Literature in English PAPER 2', 'Literature in English PAPER 2'),
    ('Literature in English PAPER 3', 'Literature in English PAPER 3'),
    # Religious Studies
    ('Religious Studies PAPER 1', 'Religious Studies PAPER 1'),
    ('Religious Studies PAPER 2', 'Religious Studies PAPER 2'),
    ('Religious Studies PAPER 3', 'Religious Studies PAPER 3'),
    # Design and Technology
    ('Design and Technology PAPER 1', 'Design and Technology PAPER 1'),
    ('Design and Technology PAPER 2', 'Design and Technology PAPER 2'),
    ('Design and Technology PAPER 3', 'Design and Technology PAPER 3'),
    # Food Technology
    ('Food Technology PAPER 1', 'Food Technology PAPER 1'),
    ('Food Technology PAPER 2', 'Food Technology PAPER 2'),
    ('Food Technology PAPER 3', 'Food Technology PAPER 3'),
]

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, choices=SUBJECT_CHOICES)

    def __str__(self):
        return self.name

class Entry(models.Model):
    student_name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    form_number = models.PositiveSmallIntegerField()  # 1-6
    student_mark = models.FloatField()
    account = models.IntegerField()

    class Meta:
        unique_together = ('student_name', 'subject', 'form_number')

    def __str__(self):
        return f'{self.student_name} - {self.subject.name} (Form {self.form_number})'
