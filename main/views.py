from django.views.generic import TemplateView
from.models import Visit
from django.utils import timezone
from datetime import timedelta
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404

from.models import UserProfile
from django.core.files.storage import default_storage
import os
import boto3
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q, Window, F
from django.db.models.functions import Rank

from django.contrib.auth.decorators import user_passes_test
import csv
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from.models import PasswordGate
from.models import FormGroup
from google.cloud import vision
from django.core.cache import cache


from django import forms
from django.contrib.auth.models import User
from.models import Subject, Entry

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from .models import Entry
from django.db.models import Count
from .models import Entry
import json
from django.shortcuts import render
from django.db.models import Sum, Count, Q


def results(request):
    passed_subjects_by_form = {}
    subjects = Entry.objects.filter(student_mark__gte=50).values_list('subject').annotate(count=Count('subject')).order_by('-count')
    passed_subjects_by_form = subjects[:20] 

    context = {
        'passed_subjects_by_form': passed_subjects_by_form,
    }
                            
        
    return render(request, 'main/res.html',  { 'passed_subjects_by_form': passed_subjects_by_form, 'subjects': subjects})





@user_passes_test(lambda u: u.is_superuser)
def delete_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        messages.success(request, f"{filename} deleted successfully.")
    else:
        messages.error(request, f"{filename} not found.")
        
    return HttpResponseRedirect(reverse('z'))    

def videoss_list(request):
    videos = Video.objects.all()
    return render(request, 'main/videoss.html', {'videos': videos})

def privacy_policy(request):
    APP_CREATED = '2026-01-10'
    last_updated = '2026-03-10'
    SILVER = "SilvertonTinotendaKuimba"
    App = 'E-RISE'
    EMAIL = 'kuimbasilverton@gmail.com'
    return render(request, 'main/video_list.html', {'APP_CREATED': APP_CREATED, 'last_updated': last_updated, 'App': App, 'SILVER': SILVER, 'EMAIL': EMAIL})





from django.db.models import Sum, Count, Q, Window, F
from django.db.models.functions import Rank
from django.shortcuts import render

def ranking(request):

    

    
            
    form_numbers = range(1, 5)
      # Forms 1 to 4
    
    # 1 QUERY: Get latest 5 entries per subject+form, then aggregate by student
    # Step 1: Get all entries for forms 1-4
    base_qs = Entry.objects.filter(form_number__in=form_numbers)
    
    # Step 2: Aggregate by student_name + form_number
    ranking_data = (
        base_qs.values('student_name', 'form_number', 'account')
        .annotate(
            total_marks=Sum('student_mark'),
            
            subjects_passed=Count('id', filter=Q(student_mark__gte=50)),
            subjectspassed=Count('id', filter=Q(student_mark__gte=1)),
            efficiency=Sum('student_mark')/Count('id', filter=Q(student_mark__gte=1))
        )
        # Step 3: Add rank PER FORM using Window function
        .annotate(
            rank=Window(
                expression=Rank(),
                 # Rank resets for each form
                order_by=F('efficiency').desc()
            )
        )
        .order_by('rank')[:100] # Top 100 overall
    )

    ranked_data = list(ranking_data)
    
        
    return render(request, 'main/ranking.html', {'ranking_data': ranked_data})
from django.db.models import Sum, Count, Q

def rankin(request):
    forms = [1, 2, 3, 4, 5, 6]
    context = {}

    for form_num in forms:
        # Get all entries for this form
        qs = Entry.objects.filter(form_number=form_num)

        # Aggregate marks by student across all subjects for this form
        ranking = (
            qs.values('student_name', 'form_number', 'account')
            .annotate(
                total_marks=Sum('student_mark'),
                subjects_passed=Count('id', filter=Q(student_mark__gte=50))
            )
            .order_by('-total_marks')
        )

        # Add rank
        ranked_list = []
        for i, student in enumerate(ranking, start=1):
            student['rank'] = i
            ranked_list.append(student)

        # Key names must match your template: ranking_data, ranking_dat, ranking_da, ranking_d, ranking_y
        if form_num == 1:
            context['ranking_data'] = ranked_list
        elif form_num == 2:
            context['ranking_dat'] = ranked_list
        elif form_num == 3:
            context['ranking_da'] = ranked_list
        elif form_num == 4:
            context['ranking_d'] = ranked_list
        elif form_num == 5:
            context['ranking_y'] = ranked_list
        elif form_num == 6:
            context['ranking_'] = ranked_list # you didn't have form 6 in template yet

    return render(request, 'main/IQ.html', context)



def serve_file(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id)
        response = HttpResponse(doc.file, content_type='application/pdf')  # change MIME type if needed
        response['Content-Disposition'] = f'inline; filename="{doc.file.name}"'
        return response
    except Document.DoesNotExist:
        raise Http404('File not found')



def uplod_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('uplod_file')  # or where you want
    else:
        form = DocumentForm()
    return render(request, 'main/uplod.html', {'form': form})


def trigger_notification(request):
    subject = 'New Assignment Posted!'
    message = 'A new assignment has been uploaded. Check the site!'
    recipient_list = list(User.objects.filter(profile__isnull=False, is_active=True).values_list('email', flat=True))# Replace with actual user emails

    send_notification_email.delay(subject, message, recipient_list)

    return render(request, 'main/notification_sent.html')

def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/notifications.html', {'notifications': notifications})

#long_task.delay()

@user_passes_test(lambda u: u.is_superuser)
def delete_file(request, file_id):
    file_obj = get_object_or_404(Document, id=file_id)
    file_obj.file.delete()  # Delete from storage
    file_obj.delete()       # Delete DB entry
    return redirect('pdf_files')  # Update to your actual view name


def math_solver_page(request):
    return render(request, 'main/chatbot.html')  # replace with your actual template name




@login_required
def splash_view(request):
    return render(request, 'main/splash_view.html')


@login_required
def home(request):
    
    return render(request, 'main/splash_view.html')
    
def biology(request):   
    return render(request, 'main/7.html')


def premium_view(request):
    return render(request, 'main/premium.html')
    
def y_view(request):
    return render(request, 'main/8.html')    

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('g')
    else:
        form = VideoUploadForm()
    return render(request, 'main/upload_video.html', {'form': form})





def manage(request):
    return render(request, 'main/manage.html')


@login_required
def check_payment(request):
    profile = UserProfile.objects.get(user=request.user)
    profile.is_premium = True
    profile.save()
    return JsonResponse({'status': 'success', 'message': 'Premium activated!'})
    





def add_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_account')

        user = User.objects.create_user(username=username, email=email, password=password)

        # Wait for signal to create the profile
        # Now safely update it
        profile, created = UserProfile.objects.get_or_create(user=user)
      
        profile.save()
        messages.success(request, 'Account created successfully!')
        return redirect('login')

    return render(request, 'main/add_account.html')

@login_required
def balance(request):
    ranking_data = Entry.objects.all()
    balance = 0
    if request.user.is_authenticated:
        try:
            entry = Entry.objects.filter(account=str(request.user.username)).all()
            balance = 25.00
            # You can also update the UserProfile model here
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.balance = 25
            user_profile.save()
        except Entry.DoesNotExist:
           
            pass
        except ValueError:
            # Handle the case where the username is not a valid integer
            
            pass
            
    return render(request, 'main/balance.html', {'balance': balance})

    
                    







def friends_view(request):
    logged_in_users = User.objects.all().select_related('profile')
    total_users = logged_in_users.count()

    form_numbers = range(1, 5) # Forms 1 to 4

    # 1 QUERY: Aggregate all entries for forms 1-4 by account
    ranking_data = (
        Entry.objects
      .filter(form_number__in=form_numbers)
      .values('account') # group by account
      .annotate(
            total_marks=Sum('student_mark'),
            subjects_passed=Count('id', filter=Q(student_mark__gte=50))
        )
      .order_by('-total_marks')[:10] # top 10
    )

    # Manual rank: 5, 4.5, 4, 3.5...
    rank_dict = {}
    rank = 5.0
    for student in ranking_data:
        account = str(student['account']) # force string key to match template
        if account and account not in rank_dict:
            rank_dict[account] = rank
            rank -= 0.5

    return render(request, 'main/friends.html', {
        'logged_in_users': logged_in_users,
        'total_users': total_users,
        'rank_dict': rank_dict # {'1405': 5.0, '1406': 4.5}
    })
@login_required
def notifications_view(request):
    return render(request, 'main/notifications.html')

@login_required
def privacy_view(request):
    return render(request, 'main/privacy.html')
    


PASSWORDS = ['123', '456', '789']  # Better: store hashes instead


@csrf_exempt
def password_gate_view(request):
    if request.method == 'POST':
        step = int(request.POST.get('step', 0))
        pw = request.POST.get('password', '')

        if step <= 0 or step > len(PASSWORDS):
            return JsonResponse({'error': 'Invalid step'}, status=400)

        if pw == PASSWORDS[step - 1]:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Incorrect password'}, status=400)

    return render(request, 'main/password_gate.html')









def register_school(request):
    if request.method == 'POST':
        name = request.POST.get('school_name')
        code = request.POST.get('school_code')
        password = request.POST.get('password')

        if name and code and password:
            hashed_password = make_password(password)
            School.objects.create(name=name, code=code, password=hashed_password)
            return redirect('group_A')  # redirect after success
        else:
            error = "Please fill all fields."
            return render(request, 'main/register.html', {'error': error})

    return render(request, 'main/register.html')

    
def admins_view(request):
    if request.method == 'POST':
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        # Replace these with your actual admin passwords
        if pw1 == '123' and pw2 == '456':
            request.session['is_admin'] = True
            return redirect('8')
        else:
            return render(request, 'main/admins.html', {'error': 'Incorrect passwords'})
    return render(request, 'main/admins.html')
    
    

def delete_school_list(request):
    if not request.session.get('is_admin'):
        return redirect('admins')  # block access if not admin

    schools = School.objects.all()
    return render(request, 'main/delete.html', {'schools': schools})

def delete_school(request, school_id):
    if not request.session.get('is_admin'):
        return redirect('admins')

    if request.method == 'POST':
        school = get_object_or_404(School, id=school_id)
        school.delete()
        messages.success(request, f'School "{school.name}" deleted successfully.')
    return redirect('delete_school_list')    
    
    
    

    
    
def submit(request):
    if request.method == 'POST':
        school_code = request.POST.get('school_code', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            school = School.objects.get(code=school_code)
            if not check_password(password, school.password):
                messages.error(request, "Invalid school code or password.")
                return redirect('submit')
            # Success: password correct
            request.session['authenticated_school'] = school_code
            return redirect('settings')
        except School.DoesNotExist:
            messages.error(request, "Invalid school code or password.")
            return redirect('submit')

    return render(request, 'main/7.html')

    
    
def account_security_view(request):
    # Get the single PasswordGate instance or create if none
    gate, _ = PasswordGate.objects.get_or_create(id=1)

    if request.method == "POST":
        current_password = request.POST.get('password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Verify current against first password step
        if not check_password(current_password, gate.password1):
            messages.error(request, "❌ ")
            return redirect('account_security')

        if new_password!= confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('account_security')

        if not new_password:
            messages.error(request, "New password cannot be empty.")
            return redirect('account_security')

        # Update all 3 steps passwords to new password encrypted
        hashed = make_password(new_password)
        gate.password1 = hashed
        
        gate.password3 = hashed
        gate.save()

        messages.success(request, "✅")
        return redirect('account_security')

    return render(request, 'main/account_security.html')

    
        
 
    




    
  
def registered_school_view(request, school_id):
    school = get_object_or_404(School, id=school_id)
    
    if school.id == 1:
        return redirect('school1_update', school_id=school_id)
    elif school.id == 2:
        return redirect('school2_update', school_id=school_id)
    elif school.id == 3:
        return redirect('school3_update', school_id=school_id)
    elif school.id == 4:
        return redirect('school4_update', school_id=school_id)
    elif school.id == 5:
        return redirect('school5_update', school_id=school_id)
    
    marks = StudentMarkArchive.objects.filter(school=school).order_by('-math_score')
    top_students = StudentMarkArchive.objects.order_by('-math_score')[:10]
    return render(request, 'main/registered.html', {'school': school, 'students': top_students, 'marks': marks})

    

    
    
def school_update_view(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    numbers = range(1, 11)
    if request.method == 'POST':
        for i in numbers:
            name = request.POST.get(f'tudent_name_{i}', '').strip()
            mark = request.POST.get(f'tudent_mark_{i}', '').strip()
            if name and mark:
                try:
                    score = int(mark)
                    student_mark, created = StudentMarkArchive.objects.update_or_create(name=name, school=school)
                    student_mark.math_score = score
                    student_mark.save()
                except ValueError:
                    messages.error(request, f"Invalid mark input for student #{i}: {mark}")                
        messages.success(request, "#{i}: {mark}")
        messages.success(request, "Marks updated successfully!")
        return redirect('registered_school', school_id=school_id)
    return render(request, 'main/your_update.html', {'school': school, 'numbers': numbers})   
    


   
def password_gate_view(request):
    gate = PasswordGate.objects.first()  # assuming only one record

    if request.method == 'POST':
        step = int(request.POST.get('step', 0))
        password = request.POST.get('password', '').strip()

        if step not in [1, 2, 3] or not password:
            return JsonResponse({'error': 'Invalid request'}, status=400)

        pw_hash = {
            1: gate.password1,
            2: gate.password2,
            3: gate.password3,
        }.get(step)

        if check_password(password, pw_hash):
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Incorrect password'}, status=400)

    return render(request, 'main/password_gate.html')



def account_security_view1(request):
    # Get the single PasswordGate instance or create if none
    gate, _ = PasswordGate.objects.get_or_create(id=1)

    if request.method == "POST":
        current_password = request.POST.get('password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Verify current against first password step
        if not check_password(current_password, gate.password1):
            messages.error(request, "❌ ")
            return redirect('acount_security')

        if new_password!= confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('acount_security')

        if not new_password:
            messages.error(request, "New password cannot be empty.")
            return redirect('acount_security')

        # Update all 3 steps passwords to new password encrypted
        hashed = make_password(new_password)
        gate.password1 = hashed
        
        gate.password3 = hashed
        gate.save()

        messages.success(request, "✅")
        return redirect('acount_security')

    return render(request, 'main/acount_security.html')






def teachers_view(request):
    for i in range(1, 7):
        FormGroup.objects.get_or_create(number=i)
    
    if request.method == "POST":
        for form_number in range(1, 7):
            form_group = FormGroup.objects.get(number=form_number)
            for i in range(1, 11):
                key = f'form{form_number}_teacher{i}'
                name = request.POST.get(key, '').strip()
                if name:
                    teachers = list(form_group.teachers.all())
                    if i-1 < len(teachers):
                        teacher = teachers[i-1]
                        teacher.name = name
                        teacher.save()
                    else:
                        Teacher.objects.create(form_group=form_group, name=name)
                else:
                    
                    pass
                    
        return redirect('teachers')  # reload page after saving
    
    # GET request: load teachers grouped by form to send to template
    teachers_by_form = []
    for form_number in range(1, 7):
        form_group = FormGroup.objects.get(number=form_number)
        teachers = list(form_group.teachers.all())
        # fill up to 10 teachers with empty if needed
        while len(teachers) < 10:
            teachers.append(Teacher(name=''))
        teachers_by_form.append({'number': form_number, 'teachers': teachers})
    
    return render(request, 'main/teachers.html', {'teachers_by_form': teachers_by_form})



def teachers_review(request):
    forms = FormGroup.objects.prefetch_related('teachers').all().order_by('number')
    return render(request, 'main/review.html', {'forms': forms})

 
    
       
def dlete(request):
    if request.method == 'POST':
        logged_in_users = UserProfile.objects.all()
        delete = logged_in_users.delete()
        messages.success(request, f'student  deleted successfully.')
    
    
    return render(request, 'main/dlete.html', {'logged_in_users': logged_in_users, 'delete': delete})

def dlete_school(request):
    

    if request.method == 'POST':
        top_students = StudentMark.objects.all()
        
        top_students.delete()
        messages.success(request, f'student  deleted successfully.')
    return redirect('dlete')                 


    
    


def cache_set_view(request):
    cache.set('my_key', 'Hello from Redis!', timeout=60)  # cache for 60 sec
    return JsonResponse({'message': 'Value cached!'})

def cache_get_view(request):
    value = cache.get('my_key')
    if value:
        return JsonResponse({'cached_value': value})
    else:
        return JsonResponse({'error': 'No cached value found'}, status=404)


        
@login_required    
def re(request):

    school_code = request.POST.get('school_code')
    password = request.POST.get('password')
        

    if not school_code or not password:
        messages.error(request, "Enter school code and password.")
        return redirect('submit')

    try:
        school = School.objects.get(code=school_code, password=password)
    except School.DoesNotExist:
        messages.error(request, "Invalid school code or password.")
        return redirect('submit')

        

        
    

        
    
    return render(request, 'main/7.html')    
    
            

    
def biology(request):
    logged_in_users = User.objects.all()
    total_users = logged_in_users.count()
    total_money = total_users * 5
    return render(request, 'main/bio.html',  {'logged_in_users': logged_in_users, 'total_users': total_users, 'total_money': total_money})    
    



def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

    





from django.shortcuts import render
from django.db.models import Sum, Count, Q, Avg
import json

def search_results(request):
    q = request.GET.get('q', '')

    # 1. Ranking data
    ranking_data = Entry.objects.values('student_name', 'form_number', 'account').annotate(
        total_marks=Sum('student_mark'),
        
        subjects_passed=Count('id', filter=Q(student_mark__gte=50)),
  
    ).order_by('-total_marks')

    # Add rank to each student
    ranked_data = []
    rank = 1
    for student in ranking_data:
        student['rank'] = rank
        ranked_data.append(student)
        rank += 1

    if q:
        results = [student for student in ranked_data if q.lower() in student['student_name'].lower()]
    else:
        results = ranked_data

    rsults = Entry.objects.filter(student_name__icontains=q)

    chart_data = None
    student_name = None
    passed_subjects = None
    failed_subjects = None
    non_recorded_subjects = None

    if rsults.exists():
        student_name = rsults[0].student_name
        subject_results = Entry.objects.filter(student_name=student_name).order_by('id') # order by id. change to 'date' if you have it

        passed_subjects = subject_results.filter(student_mark__gte=50)
        failed_subjects = subject_results.filter(Q(student_mark__lt=50))
        
        non_recorded_subjects = subject_results.filter(Q(student_mark__isnull=True))
       

        # 2. Build cumulative average starting from 0
        weeks = [0]
        averages = [0]
        cumulative_sum = 0
        count = 0

        # Get only entries with actual marks
        marks_list = [e.student_mark for e in subject_results if e.student_mark is not None]

        if marks_list: # if student has marks
            for mark in marks_list:
                cumulative_sum += mark
                count += 1
                weeks.append(count)
                averages.append(round(cumulative_sum / count, 2))
        else: # if no marks at all, still show 0 to 0 line
            weeks = [0, 1]
            averages = [0, 1]

        chart_data = json.dumps({'labels': weeks, 'data': averages})

        # DEBUG - remove after testing
        print(f"DEBUG: Student: {student_name}")
        print(f"DEBUG: Marks: {marks_list}")
        print(f"DEBUG: Chart: {chart_data}")

    context = {
        'results': results,
        'query': q,
        'rsults': rsults,
        'passed_subjects': passed_subjects,
        'failed_subjects': failed_subjects,
        'non': non_recorded_subjects,
        'student_name': student_name,
        'chart_data': chart_data,
    }

    return render(request, 'main/search_results.html', context)
    
def enter_marks(request, subject_id, form_number):
    subject = get_object_or_404(Subject, id=subject_id)
    existing_marks = Entry.objects.filter(subject=subject, form_number=form_number)

    if request.method == 'POST':
        student_names = request.POST.getlist('student_name')
        marks = request.POST.getlist('marks')

        if len(student_names) != len(marks):
            return render(request, 'main/enter_marks.html', {
                'subject': subject,
                'form': form_number,
                'error': "Mismatch in number of students and marks",
                'existing_marks': existing_marks
            })

        for name, mark in zip(student_names, marks):
            if name.strip() == '' or not mark.isdigit() or not (0 <= int(mark) <= 100):
                continue  # Skip invalid input
                Entry.objects.update_or_create(
                student_name=name.strip(),
                subject=subject,
                form_number=form_number,
                defaults={'student_mark': int(mark)}
            )

        return redirect('results')  # Adjust to your actual redirect target

    return render(request, 'main/enter_marks.html', {
        'subject': subject,
        'form': form_number,
        'existing_marks': existing_marks,
    })

    
from django.db.models import Sum, Count, Q

def rank(request):
    forms = [1, 2, 3, 4, 5, 6]
    context = {}
    q = request.GET.get('q', '')
   

    for form_num in forms:
        # Get all entries for this form
        qs = Entry.objects.filter(form_number=form_num)

        # Aggregate marks by student across all subjects for this form
        ranking = (
            qs.values('student_name', 'form_number', 'account')
            .annotate(
                total_marks=Sum('student_mark'),
                subjects_passed=Count('id', filter=Q(student_mark__gte=50)),
                subjectspassed=Count('id', filter=Q(student_mark__gte=1)),
                efficiency=Sum('student_mark')/Count('id', filter=Q(student_mark__gte=1))
            )
            .order_by('-total_marks')
        )

        # Add rank
        ranked_list = []
        for i, student in enumerate(ranking, start=1):
            student['rank'] = i
            ranked_list.append(student)

        # Key names must match your template: ranking_data, ranking_dat, ranking_da, ranking_d, ranking_y
        if form_num == 1:
            context['ranking_data'] = ranked_list
        elif form_num == 2:
            context['ranking_dat'] = ranked_list
        elif form_num == 3:
            context['ranking_da'] = ranked_list
        elif form_num == 4:
            context['ranking_d'] = ranked_list
        elif form_num == 5:
            context['ranking_y'] = ranked_list
        elif form_num == 6:
            context['ranking_'] = ranked_list # you didn't have form 6 in template yet

    return render(request, 'main/show_files.html', context)




    
@login_required

def student_results(request):
    usr = UserProfile.objects.filter(username)
    if usr == entry.account:
        query == 'usr'
    else:    
        query = request.GET.get('q')
    if query:
        entries = Entry.objects.filter(student_name__icontains=query)
        results = {}
        for entry in entries:
            if entry.student_name not in results:
                results[entry.student_name] = {'passed': [], 'failed': []}
            if entry.student_mark >= 50:
                results[entry.student_name]['passed'].append(entry.subject.name)
            
            else:
                results[entry.student_name]['failed'].append(entry.subject.name)
        context = {
            'query': query,
            'results': results,
        }
        return render(request, 'main/search_results.html', context)
    else:
        return render(request, 'main/search_results.html', {})
        
        
# adjust this import to match your model
def analysis(request):
    
 
    form_numbers = range(1, 7)  # Update range as needed
    subjects = Subject.objects.all()
    data = {}
    
    subject_scores = {subject.name: 0 for subject in subjects}

    for form_num in form_numbers:
        data[form_num] = {}
        for subject in subjects:
            entries = Entry.objects.filter(subject=subject, form_number=form_num).order_by('-id')[:200]
            data[form_num][subject] = entries

            # Sum marks for analysis
            total = sum(entry.student_mark for entry in entries)
            subject_scores[subject.name] += total
    

    context = {
        'form_numbers': form_numbers,
        'subjects': subjects,
        'data': data,
    }
    return redirect('login')
    return render(request, 'main/analysis.html', {'form_numbers': form_numbers, 'subjects': subjects, 'data': data})
    
    


def pdf_list(request):
    files = Document.objects.filter(file__iendswith='.pdf')
    return render(request, 'main/z.html', {'files': files})
    
    


    
 

def search_pdfs(request):
    query = request.GET.get('q', '')
    files = Document.objects.filter(file__icontains=query) if query else Document.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'main/ab.html', {'files': files})

    return render(request, 'main/z.html', {'files': files, 'query': query})    
  
  
def serch_pdfs(request):
    query = request.GET.get('q', '')
    videos = Video.objects.filter(title__icontains=query) if query else Video.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'main/ac.html', {'videos': videos})

    return render(request, 'main/z.html', {'videos': videos, 'query': query})    
    



def df_list(request):
    files = Document.objects.filter(file__iendswith='.pdf')
    return render(request, 'main/show_files.html', {'files': files})

def f_list(request):
    files = Document.objects.filter(file__iendswith='.pdf')
    return render(request, 'main/show_files.html', {'files': files})    
 

def search_dfs(request):
    query = request.GET.get('q', '')
    files = UploadedFile.objects.filter(file__icontains=query) if query else UploadedFile.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'main/qa.html', {'files': files})

    return render(request, 'main/res.html', {'files': files, 'query': query})   



def search_fs(request):
    query = request.GET.get('q', '')
    student_name = Entry.objects.filter(student_name__icontains=query) if query else Entry.objects.all()
    form_number = Entry.objects.filter(form_number__icontains=query) if query else Entry.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'main/qaw.html', {'student_name': student_name, 'form_number': form_number})

    return render(request, 'main/ranking.html', {'student_name': student_name, 'form_number': form_number, 'query': query})   
    
    
    