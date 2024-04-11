from django.urls import path
from . import views

urlpatterns = [
  path('jobs/', views.jobs, name='jobs'),
  path('view_application/<str:job_application_id>', views.view_application, name='view-application'),
  
  path('recruiter/create_job/', views.create_job, name='create-job'),
  path('recruiter/update_job/<str:job_id>', views.update_job, name='update-job'),
  
  path('candidate/applications/applied', views.candidate_applied_applications, name='candidate-applied-applications'),
  path('candidate/applications/screening', views.candidate_screening_applications, name='candidate-screening-applications'),
  path('candidate/applications/interview', views.candidate_interview_applications, name='candidate-interview-applications'),
  path('candidate/applications/accepted', views.candidate_accepted_applications, name='candidate-accepted-applications'),
  path('candidate/applications/rejected', views.candidate_rejected_applications, name='candidate-rejected-applications'),
  
  # API
  path('api/change_job_status/<str:job_id>', views.change_job_status, name='change-job-status'),
  path('api/apply_job/<str:job_id>', views.apply_job, name='candidate-apply-job'),
]