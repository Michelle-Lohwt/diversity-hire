from django.urls import path
from . import views

urlpatterns = [
  path('jobs/', views.jobs, name='jobs'),
  
  path('recruiter/create_job/', views.create_job, name='create-job'),
  path('recruiter/update_job/<str:job_id>', views.update_job, name='update-job'),
  
  path('applications/applied', views.view_applied_applications, name='view-applied-applications'),
  path('applications/screening', views.view_screening_applications, name='view-screening-applications'),
  path('applications/interview', views.view_interview_applications, name='view-interview-applications'),
  path('applications/accepted', views.view_accepted_applications, name='view-accepted-applications'),
  path('applications/rejected', views.view_rejected_applications, name='view-rejected-applications'),
  path('view_application/<str:job_application_id>', views.view_application, name='view-application'),
  
  # API
  path('api/change_job_status/<str:job_id>', views.change_job_status, name='change-job-status'),
  path('api/apply_job/<str:job_id>', views.apply_job, name='candidate-apply-job'),
]