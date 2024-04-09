from django.urls import path
from . import views

urlpatterns = [
  path('jobs/', views.jobs, name='jobs'),
  
  path('recruiter/create_job/', views.create_job, name='create-job'),
  path('recruiter/update_job/<str:job_id>', views.update_job, name='update-job'),
  
  path('view_application/<str:job_application_id>', views.view_application, name='view-application'),
  
  # API
  path('api/change_job_status/<str:job_id>', views.change_job_status, name='change-job-status'),
  path('api/apply_job/<str:job_id>', views.apply_job, name='candidate-apply-job'),
]