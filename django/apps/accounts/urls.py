from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.loginPage, name='login'),
  path('logout/', views.logoutUser, name='logout'),
  path('update_profile/', views.update_profile, name='update-profile'),
  # path('view_profile/', views.view_profile, name='view-profile'),
  
  path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter-dashboard'),
  path('recruiter/jobs/<str:job_id>', views.recruiter_jobs, name='recruiter-jobs'),
  # path('recruiter/candidates', views.recruiter_candidates, name='recruiter-candidates'),
  
  path('candidate/dashboard/', views.candidate_dashboard, name='candidate-dashboard'),
  
  
  # API
  path('api/get_job_details/<str:job_id>', views.get_job_details, name='get-job-details'),
  
  # Test
  # path('candidate/update_profile/<str:pk>', views.CandidateProfileUpdate.as_view(), name='update-candidate-profile'),
  # path('delete_experience/<str:exp_id>', views.delete_experience, name='delete-experience')
]