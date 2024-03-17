from django.urls import path
from . import views

urlpatterns = [
  path('jobs/', views.jobs, name='jobs'),
  
  path('recruiter/<str:pk>/create_job/', views.create_job, name='create-job'),
  path('recruiter/<str:pk>/update_job/<str:job_id>', views.update_job, name='update-job'),
  
  path('api/change_job_status/<str:job_id>', views.change_job_status, name='change-job-status'),
]