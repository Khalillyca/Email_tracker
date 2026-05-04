from django.contrib import admin
from django.urls import path
from tracker_app.views import email_tracker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/email-tracker/', email_tracker, name='email_tracker'),
]
