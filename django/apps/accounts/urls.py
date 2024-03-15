from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  # path('logout/', views.logout, name='logout'),
  
  path('recruiter/<str:pk>/dashboard/', views.recruiter_dashboard, name='recruiter-dashboard'),
  path('recruiter/<str:pk>/jobs/<str:job_id>', views.recruiter_jobs, name='recruiter-jobs'),
  # path('recruiter/candidates', views.recruiter_candidates, name='recruiter-candidates'),
  
  path('candidate/dashboard/', views.candidate_dashboard, name='candidate-dashboard'),
  # path('edit_profile/', views.edit_profile, name='edit_profile'),
  
  # API
  path('api/get_job_details/<str:job_id>', views.get_job_details, name='get-job-details')
]