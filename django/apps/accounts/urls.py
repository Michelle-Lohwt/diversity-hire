from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.loginPage, name='login'),
  path('logout/', views.logoutUser, name='logout'),
  
  path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter-dashboard'),
  path('recruiter/jobs/<str:job_id>', views.recruiter_jobs, name='recruiter-jobs'),
  # path('recruiter/candidates', views.recruiter_candidates, name='recruiter-candidates'),
  
  path('candidate/dashboard/', views.candidate_dashboard, name='candidate-dashboard'),
  # path('edit_profile/', views.edit_profile, name='edit_profile'),
  
  # API
  path('api/get_job_details/<str:job_id>', views.get_job_details, name='get-job-details')
]