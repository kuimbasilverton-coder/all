
from django.contrib import admin
from django.urls import include, path
from main import views
from django.conf import settings
from django.conf.urls.static import static
from main.views import friends_view

from main.views import registered_school_view, school_update_view
from django.contrib.auth import views as auth_views
from main.views import password_gate_view, account_security_view1
from main.views import account_security_view
from main.views import teachers_view
from main.views import teachers_review
from main.views import dlete_school
#from main.views import dlte_school
from main.views import add_account


from main.views import serve_file

from main.views import uplod_file
from main.views import manage
urlpatterns = [
    path('admin/', admin.site.urls),
    path('uplod/', views.uplod_file, name='uplod_file'),
    path('pdfs/', views.search_pdfs, name='pdf_search'),
    path('dfs/', views.search_dfs, name='df_search'),
    path('pdfss/', views.serch_pdfs, name='pdf_serch'),
    path('dfs/', views.search_dfs, name='df_search'),
    path('fs/', views.search_fs, name='f_search'),
    path('privacy_policy/', views.privacy_policy, name='f'),
    path('videoss_list/', views.videoss_list, name='g'),
    path('balance/', views.balance, name='balance'),
    
    
    path('manage/', views.manage, name='manage'),
    path('', views.splash_view, name='splash'), 
    path('pdfs/', views.pdf_list, name='z'),
    path('y/', views.y_view, name='8'),    
    # Premium & payment
    path('premium/', views.premium_view, name='premium'),
    path('re/', views.re, name='re'),
    # User & file management
    path('add-account/', views.add_account, name='add_account'),
    path('departments/submit/', views.submit, name='submit'),
    
    path('upload_video/', views.upload_video, name='upload_video'),
  
    path('friends/', views.friends_view, name='friends'),
    
    path('settings/security/', views.account_security_view, name='account_security'),
    
    path('settings/notifications/', views.notifications_view, name='notifications'),
    path('settings/privacy/', views.privacy_view, name='privacy'),
    path('password-gate/', views.password_gate_view, name='password_gate'),
    path('register/', views.register_school, name='register'),
    path('admins/', views.admins_view, name='admins'),
    path('delete/', views.delete_school_list, name='delete_school_list'),
    path('delete/<int:school_id>/', views.delete_school, name='delete_school'),
    path('dlete/', views.dlete, name='dlete'),
    
    path('settings/account-security/', account_security_view, name='account_security'),
    path('rnk', views.rank, name='show'),
    
    path('dlete', views.dlete_school, name='dlete_school'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/logn.html'), name='logn'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/logn.html'), name='logn'),
    path('school/<int:school_id>/', views.registered_school_view, name='registered_school'),
    path('school/update/<int:school_id>/', views.school_update_view, name='school_update'),
   
   
    path('password-gate/', password_gate_view, name='password_gate'),
    path('acount-security/', account_security_view1, name='acount_security'),
   
    
    path('teachers/', teachers_view, name='teachers'),
    path('techers/', teachers_review, name='review'),
    path('cache-set/', views.cache_set_view, name='cache_set'),
    path('cache-get/', views.cache_get_view, name='cache_get'), 
    path('file/<int:doc_id>/', views.serve_file, name='serve_file'),
    path('', views.home, name='home'),  # Your homepage
    path('results/', views.results, name='results'),
    path('subjects/', views.subject_list, name='subjects'),
    
    path('renk/', views.ranking, name='ranking'),
    path('rankin/', views.rankin, name='rankin'),
    # Dynamic URL to handle all subjects + forms (form_number 1 to 6)
    path('enter/<int:subject_id>/form/<int:form_number>/', views.enter_marks, name='enter_marks'),
    path('biology/', views.biology, name='biology'),
    path('results/', views.results, name='results'),
    path('search/', views.search_results, name='search_results'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    




    







    
   
