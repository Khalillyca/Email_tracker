from django.contrib import admin
from django.urls import path
from tracker_app.views import EmailTrackerView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Map the endpoint exactly as expected by your Flask backend
    path('api/email-tracker/', EmailTrackerView.as_view(), name='email_tracker'),
]
