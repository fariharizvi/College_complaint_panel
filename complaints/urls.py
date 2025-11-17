from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    # ⭐ Submit Complaint URL (this was missing earlier)
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('view-complaints/', views.view_complaints, name='view_complaints'),

    path('logout/', views.user_logout, name='logout'),
]
