"""
Definition of urls for CUCOMProject.
"""

from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    
    # Authentication paths
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    
    path('student-entry/', views.StudentEntry.as_view(), name='student-entry'),
    path('students/', views.StudentsTableView.as_view(), name='students'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    
    # Email sending paths
    path('send_registration_mail/<int:pk>/', views.SendRegistrationMail.as_view(), name='send_registration_mail'),
    path('send_resource_mail/<int:pk>/', views.SendResourceMail.as_view(), name='send_resource_mail'),

    path('upcoming/', views.UpcomingView.as_view(), name='upcoming'),
    path('delete/<int:pk>/', views.delete_student, name='delete'),
    path('genqr/<int:pk>/', views.GenQR.as_view(), name='generate_qr_code'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
