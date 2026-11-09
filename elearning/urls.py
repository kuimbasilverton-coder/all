from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home / splash - you have 2, splash is firs
    path('', views.splash_view, name='splash'),
    path('home/', views.home, name='home'),
    
  
    path('pdfs/', views.search_pdfs, name='pdf_search'),
    path('dfs/', views.search_dfs, name='df_search'),
    path('pdfss/', views.serch_pdfs, name='pdf_serch'),
    path('dfs/', views.search_dfs, name='df_search'),
    path('fs/', views.search_fs, name='f_search'),

    # Results / ranking / search / marks
    path('results/', views.results, name='results'),
    path('renk/', views.ranking, name='ranking'),
    path('rankin/', views.rankin, name='rankin'),
    path('rnk/', views.rank, name='show'),
    path('search/', views.search_results, name='search_results'),
    path('enter/<int:subject_id>/form/<int:form_number>/', views.enter_marks, name='enter_marks'),
    path('analysis/', views.analysis, name='analysis'),
    path('biology/', views.biology, name='biology'),

    # Pages
    path('privacy_policy/', views.privacy_policy, name='f'),
    path('premium/', views.premium_view, name='premium'),
    path('y/', views.y_view, name='8'),
    path('manage/', views.manage, name='manage'),
    path('balance/', views.balance, name='balance'),
    path('check-payment/', views.check_payment, name='check_payment'),
    path('friends/', views.friends_view, name='friends'),
    path('math-solver/', views.math_solver_page, name='math_solver'),

    # Accounts
    path('add-account/', views.add_account, name='add_account'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('dlete/', views.dlete, name='dlete'),

    # Settings / security
    path('settings/security/', views.account_security_view, name='account_security'),
    path('settings/notifications/', views.notifications_view, name='notifications'),
    path('settings/privacy/', views.privacy_view, name='privacy'),
    path('password-gate/', views.password_gate_view, name='password_gate'),

    # Cache test
    path('cache-set/', views.cache_set_view, name='cache_set'),
    path('cache-get/', views.cache_get_view, name='cache_get'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)