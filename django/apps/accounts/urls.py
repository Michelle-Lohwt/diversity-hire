from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.loginPage, name='login'),
  path('logout/', views.logoutUser, name='logout'),
  
  path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter-dashboard'),
  path('recruiter/profile/<str:last_login>', views.update_recruiter_profile, name='recruiter-profile'),
  path('recruiter/company/<str:last_login>', views.update_recruiter_company, name='recruiter-company'),
  
  path('candidate/dashboard/', views.candidate_dashboard, name='candidate-dashboard'),
  path('candidate/profile/<str:last_login>', views.update_candidate_profile, name='candidate-profile'),
  path('candidate/skills/<str:last_login>', views.update_candidate_skills, name='candidate-skills'),
  path('candidate/educations/<str:last_login>', views.update_candidate_educations, name='candidate-educations'),
  path('candidate/experiences/<str:last_login>', views.update_candidate_experiences, name='candidate-experiences'),
  
  
  # API
  path('api/get_job_details/<str:job_id>', views.get_job_details, name='get-job-details'),
  
]