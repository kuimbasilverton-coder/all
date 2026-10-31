
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')  # use your project’s settings module
django.setup()

from main.models import PasswordGate
from django.contrib.auth.hashers import make_password



pw1 = make_password('123')
pw2 = make_password('456')
pw3 = make_password('789')

PasswordGate.objects.create(password1=pw1, password2=pw2, password3=pw3)
