
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
    password1 = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)
    password3 = models.CharField(max_length=128)

    def __str__(self):
        return "Password Gate Config"

class FormGroup(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f'Form {self.number}'





        



 

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

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
                                                       
                                                                                                                                                                                                                 
  




