from django.urls import path
from . import views

urlpatterns = [
  path('jobs/', views.jobs, name='jobs'),
  path('view_application/<str:job_application_id>', views.view_application, name='view-application'),
  
  path('recruiter/create_job/', views.create_job, name='create-job'),
  path('recruiter/update_job/<str:job_id>', views.update_job, name='update-job'),
  
  path('recruiter/jobs/<str:job_id>', views.recruiter_job, name='recruiter-job'),
  path('recruiter/jobs/screening/<str:job_id>', views.recruiter_screening_job, name='recruiter-screening-job'),
  path('recruiter/jobs/interview/<str:job_id>', views.recruiter_interview_job, name='recruiter-interview-job'),
  path('recruiter/jobs/accepted/<str:job_id>', views.recruiter_accepted_job, name='recruiter-accepted-job'),
  path('recruiter/jobs/rejected/<str:job_id>', views.recruiter_rejected_job, name='recruiter-rejected-job'),
  
  path('candidate/applications/applied', views.candidate_applied_applications, name='candidate-applied-applications'),
  path('candidate/applications/screening', views.candidate_screening_applications, name='candidate-screening-applications'),
  path('candidate/applications/interview', views.candidate_interview_applications, name='candidate-interview-applications'),
  path('candidate/applications/accepted', views.candidate_accepted_applications, name='candidate-accepted-applications'),
  path('candidate/applications/rejected', views.candidate_rejected_applications, name='candidate-rejected-applications'),
  
  # API
  path('api/change_job_status/<str:job_id>', views.change_job_status, name='change-job-status'),
  path('api/apply_job/<str:job_id>', views.apply_job, name='candidate-apply-job'),
]