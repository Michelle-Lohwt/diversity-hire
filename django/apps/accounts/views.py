from django.shortcuts import render
from .models import Recruiter
from ..jobs.models import Job, JobApplication
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
  return render(request, 'home.html')

def register(request):
  return render(request, 'accounts/register.html')

def login(request):
  return render(request, 'accounts/login.html')

def recruiter_dashboard(request, pk):
  recruiter = Recruiter.objects.get(id=pk)
  # ToDo (high): change to filter the objects 
  #   that is created by the recruiter account
  jobs = Job.objects.filter(created_by = recruiter)
  # jobs = recruiter.order_set.all()
  applications = JobApplication.objects.all()
  
  total_jobs = jobs.count()
  
  # total_applications = applications.count()
  # applied = applications.filter('Applied').count()
  # screening = applications.filter('Screening').count()
  # interview = applications.filter('Interview').count()
  # accepted = applications.filter('Accepted').count()
  # rejected = applications.filter('Rejected').count()
  
  p = Paginator(jobs, 10)
  page_number = request.GET.get('page')
  
  try:
    page_job = p.get_page(page_number)
  except PageNotAnInteger:
    page_job = p.page(1)
  except EmptyPage:
    page_job = p.page(p.num_pages)
  
  context = {
    'recruiter': recruiter,
    'page_obj': page_job, 
    'applications': applications,
    'total_jobs': total_jobs,
  }
  return render(request, 'accounts/recruiter/dashboard.html', context)

# def recruiter_jobs(request):
#   return render(request, 'accounts/recruiter/dashboard.html')

# def recruiter_candidates(request):
#   return render(request, 'accounts/recruiter/dashboard.html')

def candidate_dashboard(request):
  return render(request, 'accounts/candidate/dashboard.html')