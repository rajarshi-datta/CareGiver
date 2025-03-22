from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_login/', views.user_login, name='user_login'),  
    path('user_logout/', views.user_logout, name='user_logout'),
    path('resident_dashboard/', views.resident_dashboard, name='resident_dashboard'),
    path('message_dashboard/', views.message_dashboard, name='message_dashboard'),
    path('resident_profile/', views.resident_profile, name='resident_profile'),
    path('healthcare_status/', views.healthcare_status, name='healthcare_status'),
    path('care_giver/', views.care_giver, name='care_giver'),
    path('caregiver_signup/', views.caregiver_signup, name='caregiver_signup'),
    path('caregiver_login/', views.caregiver_login, name='caregiver_login'),
    path('caregiver_dashboard/', views.caregiver_dashboard, name='caregiver_dashboard'),
    path('dashboard/', views.resident_dashboard, name='resident_dashboard'),
    path('update_health_status/', views.update_health_status, name='update_health_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
