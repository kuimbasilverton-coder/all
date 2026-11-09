from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Q, Window, F, Avg
from django.db.models.functions import Rank
from django.core.cache import cache
from django.urls import reverse
from .models import Visit, UserProfile, PasswordGate, FormGroup, Subject, Entry
import json
import csv
import os

def results(request):
    subjects = Entry.objects.filter(student_mark__gte=50).values_list('subject').annotate(count=Count('subject')).order_by('-count')
    passed_subjects_by_form = subjects[:20]
    return render(request, 'main/res.html', {'passed_subjects_by_form': passed_subjects_by_form, 'subjects': subjects})

def privacy_policy(request):
    APP_CREATED = '2026-01-10'
    last_updated = '2026-03-10'
    SILVER = "SilvertonTinotendaKuimba"
    App = 'E-RISE'
    EMAIL = 'kuimbasilverton@gmail.com'
    return render(request, 'main/video_list.html', {'APP_CREATED': APP_CREATED, 'last_updated': last_updated, 'App': App, 'SILVER': SILVER, 'EMAIL': EMAIL})

def ranking(request):
    form_numbers = range(1, 5)
    base_qs = Entry.objects.filter(form_number__in=form_numbers)
    ranking_data = (
        base_qs.values('student_name', 'form_number', 'account')
        .annotate(
            total_marks=Sum('student_mark'),
            subjects_passed=Count('id', filter=Q(student_mark__gte=50)),
            subjectspassed=Count('id', filter=Q(student_mark__gte=1)),
            efficiency=Sum('student_mark') / Count('id', filter=Q(student_mark__gte=1))
        )
        .annotate(
            rank=Window(expression=Rank(), order_by=F('efficiency').desc())
        )
        .order_by('rank')[:100]
    )
    ranked_data = list(ranking_data)
    return render(request, 'main/ranking.html', {'ranking_data': ranked_data})

def rankin(request):
    forms = [1, 2, 3, 4, 5, 6]
    context = {}
    for form_num in forms:
        qs = Entry.objects.filter(form_number=form_num)
        ranking = (
            qs.values('student_name', 'form_number', 'account')
            .annotate(
                total_marks=Sum('student_mark'),
                subjects_passed=Count('id', filter=Q(student_mark__gte=50))
            )
            .order_by('-total_marks')
        )
        ranked_list = []
        for i, student in enumerate(ranking, start=1):
            student['rank'] = i
            ranked_list.append(student)
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
            context['ranking_'] = ranked_list
    return render(request, 'main/IQ.html', context)

def math_solver_page(request):
    return render(request, 'main/chatbot.html')


def splash_view(request):
    return render(request, 'main/splash_view.html')

@login_required
def home(request):
    return render(request, 'main/splash_view.html')

def biology(request):
    logged_in_users = User.objects.all()
    total_users = logged_in_users.count()
    total_money = total_users * 5
    return render(request, 'main/bio.html', {'logged_in_users': logged_in_users, 'total_users': total_users, 'total_money': total_money})

def premium_view(request):
    return render(request, 'main/premium.html')

def y_view(request):
    return render(request, 'main/8.html')

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
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.save()
        messages.success(request, 'Account created successfully!')
        return redirect('login')
    return render(request, 'main/add_account.html')

@login_required
def balance(request):
    balance = 0
    if request.user.is_authenticated:
        try:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.balance = 25
            user_profile.save()
            balance = 25.00
        except ValueError:
            pass
    return render(request, 'main/balance.html', {'balance': balance})

def friends_view(request):
    logged_in_users = User.objects.all().select_related('profile')
    total_users = logged_in_users.count()
    form_numbers = range(1, 5)
    ranking_data = (
        Entry.objects
        .filter(form_number__in=form_numbers)
        .values('account')
        .annotate(
            total_marks=Sum('student_mark'),
            subjects_passed=Count('id', filter=Q(student_mark__gte=50))
        )
        .order_by('-total_marks')[:10]
    )
    rank_dict = {}
    rank = 5.0
    for student in ranking_data:
        account = str(student['account'])
        if account and account not in rank_dict:
            rank_dict[account] = rank
            rank -= 0.5
    return render(request, 'main/friends.html', {
        'logged_in_users': logged_in_users,
        'total_users': total_users,
        'rank_dict': rank_dict
    })

@login_required
def notifications_view(request):
    return render(request, 'main/notifications.html')

@login_required
def privacy_view(request):
    return render(request, 'main/privacy.html')

PASSWORDS = ['123', '456', '789']

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

def account_security_view(request):
    gate, _ = PasswordGate.objects.get_or_create(id=1)
    if request.method == "POST":
        current_password = request.POST.get('password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        if not check_password(current_password, gate.password1):
            messages.error(request, "Wrong current password")
            return redirect('account_security')
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('account_security')
        if not new_password:
            messages.error(request, "New password cannot be empty.")
            return redirect('account_security')
        hashed = make_password(new_password)
        gate.password1 = hashed
        gate.password2 = hashed
        gate.password3 = hashed
        gate.save()
        messages.success(request, "Password updated")
        return redirect('account_security')
    return render(request, 'main/account_security.html')

def dlete(request):
    logged_in_users = UserProfile.objects.all()
    delete = None
    if request.method == 'POST':
        delete = logged_in_users.delete()
        messages.success(request, 'Student deleted successfully.')
    return render(request, 'main/dlete.html', {'logged_in_users': logged_in_users, 'delete': delete})

def cache_set_view(request):
    cache.set('my_key', 'Hello from Redis!', timeout=60)
    return JsonResponse({'message': 'Value cached!'})

def cache_get_view(request):
    value = cache.get('my_key')
    if value:
        return JsonResponse({'cached_value': value})
    else:
        return JsonResponse({'error': 'No cached value found'}, status=404)



def search_results(request):
    q = request.GET.get('q', '')
    ranking_data = Entry.objects.values('student_name', 'form_number', 'account').annotate(
        total_marks=Sum('student_mark'),
        subjects_passed=Count('id', filter=Q(student_mark__gte=50)),
    ).order_by('-total_marks')
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
    final_grades = []
    grouped_results = []
    subject_results = None

    if rsults.exists():
        student_name = rsults[0].student_name
        subject_results = Entry.objects.filter(student_name=student_name).order_by('id')
        rsults = subject_results

        passed_subjects = subject_results.filter(student_mark__gte=50)
        failed_subjects = subject_results.filter(Q(student_mark__lt=50))
        non_recorded_subjects = subject_results.filter(Q(student_mark__isnull=True))

        # ---- FINAL GRADE LOGIC - ONE GRADE FOR 2 PAPERS ----
        def get_grade(mark):
            if mark is None:
                return '-'
            if mark >= 70:
                return 'A'
            if mark >= 60:
                return 'B'
            if mark >= 50:
                return 'C'
            if mark >= 40:
                return 'D'
            return 'F'

        from collections import defaultdict
        groups = defaultdict(list)
        for e in subject_results:
            # MATHS PAPER 1 -> MATHS, SCIENCE PAPER 2 -> SCIENCE
            base = e.subject.name.replace(' PAPER 1', '').replace(' PAPER 2', '').replace(' PAPER 3', '').strip()
            e.paper_grade = get_grade(e.student_mark)
            groups[base].append(e)

        for base, papers in groups.items():
            marks = [p.student_mark or 0 for p in papers]
            avg = sum(marks) / len(marks) if marks else 0
            fg = get_grade(avg)
            grade_colors = {'A': 'blue', 'B': '#004080', 'C': 'purple', 'D': 'orange', 'E': 'red', 'F': 'red', 'U': 'red'}
            grouped_results.append({
                'subject': base,
                'papers': papers,
                'average': round(avg, 1),
                'final_grade': fg,
                'final_color': grade_colors.get(fg, 'black'),
                'rowspan': len(papers),
            })
           
            final_grades.append({
                'subject': base,
                'average': round(avg, 1),
                'final_grade': fg,
            })
        # ---- END FINAL GRADE ----

        weeks = [0]
        averages = [0]
        cumulative_sum = 0
        count = 0
        marks_list = [e.student_mark for e in subject_results if e.student_mark is not None]
        if marks_list:
            for mark in marks_list:
                cumulative_sum += mark
                count += 1
                weeks.append(count)
                averages.append(round(cumulative_sum / count, 2))
        else:
            weeks = [0, 1]
            averages = [0, 1]
        chart_data = json.dumps({'labels': weeks, 'data': averages})

    context = {
        'results': results,
        'query': q,
        'rsults': rsults,
        'passed_subjects': passed_subjects,
        'failed_subjects': failed_subjects,
        'non': non_recorded_subjects,
        'student_name': student_name,
        'chart_data': chart_data,
        'final_grades': final_grades,
        'grouped_results': grouped_results,
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
                continue
            Entry.objects.update_or_create(
                student_name=name.strip(),
                subject=subject,
                form_number=form_number,
                defaults={'student_mark': int(mark), 'account': 0}
            )
        return redirect('results')
    return render(request, 'main/enter_marks.html', {
        'subject': subject,
        'form': form_number,
        'existing_marks': existing_marks,
    })

def rank(request):
    forms = [1, 2, 3, 4, 5, 6]
    context = {}
    for form_num in forms:
        qs = Entry.objects.filter(form_number=form_num)
        ranking = (
            qs.values('student_name', 'form_number', 'account')
            .annotate(
                total_marks=Sum('student_mark'),
                subjects_passed=Count('id', filter=Q(student_mark__gte=50)),
                subjectspassed=Count('id', filter=Q(student_mark__gte=1)),
                efficiency=Sum('student_mark') / Count('id', filter=Q(student_mark__gte=1))
            )
            .order_by('-total_marks')
        )
        ranked_list = []
        for i, student in enumerate(ranking, start=1):
            student['rank'] = i
            ranked_list.append(student)
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
            context['ranking_'] = ranked_list
    return render(request, 'main/show_files.html', context)

def analysis(request):
    form_numbers = range(1, 7)
    subjects = Subject.objects.all()
    data = {}
    for form_num in form_numbers:
        data[form_num] = {}
        for subject in subjects:
            entries = Entry.objects.filter(subject=subject, form_number=form_num).order_by('-id')[:200]
            data[form_num][subject] = entries
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
        