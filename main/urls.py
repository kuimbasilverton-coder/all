
from django.urls import path
from. import views
from main.views import (home, add_account, submit)

urlpatterns = [
    path('upload-video/', views.upload_video, name='upload_video'),
    path('', home, name='home'),
    path('add-account/', add_account, name='add_account'),
    path('submit/', submit, name='submit'),
    # add other app URLs here
]
