from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
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
  jobs = Job.objects.filter(created_by = recruiter)
  
  p = Paginator(jobs, 10)
  page_number = request.GET.get('page')
  
  try:
    page_job = p.get_page(page_number)
  except PageNotAnInteger:
    page_job = p.page(1)
  except EmptyPage:
    page_job = p.page(p.num_pages)
    
    
  selected_job_obj = page_job[0]
  applications = JobApplication.objects.all()
  
  request.user.id = pk
  request.session['job_id'] = selected_job_obj.pk
  total_jobs = jobs.count()
  
  # total_applications = applications.count()
  # applied = applications.filter('Applied').count()
  # screening = applications.filter('Screening').count()
  # interview = applications.filter('Interview').count()
  # accepted = applications.filter('Accepted').count()
  # rejected = applications.filter('Rejected').count()
  
  context = {
    'recruiter': recruiter,
    'page_obj': page_job, 
    'selected_job_obj': selected_job_obj,
    'applications': applications,
    'total_jobs': total_jobs,
  }
  return render(request, 'accounts/recruiter/dashboard.html', context)

def recruiter_jobs(request, pk, job_id = None):
  recruiter = Recruiter.objects.get(id=pk)
  request.user.id = pk
  jobs = Job.objects.filter(created_by = recruiter)
  
  # if job_id == None:
  #   jobs = jobs.first()
  # else:
  #   jobs = jobs.filter(job_id)
  
  return render(request, 'accounts/recruiter/jobs.html')

# def recruiter_candidates(request):
#   return render(request, 'accounts/recruiter/dashboard.html')

def candidate_dashboard(request):
  return render(request, 'accounts/candidate/dashboard.html')

def get_job_details(request, job_id):
  if request.method == 'GET':
    try:
      job = Job.objects.get(pk=job_id)
      try:
        q_type = job.job_required_qualifications.values('qualification_type').distinct()
        q_name = job.job_required_qualifications.values('qualification_name').distinct()
        q_list = []
        for q in q_name:
          q_list.append(q_type[0]['qualification_type'] + '/ ' + q_type[1]['qualification_type'] + ' in ' + q['qualification_name'])
      except:
        q_list = None
      
      try:
        s_list = []
        for skill in job.job_required_skills.values():
          s_list.append(skill['skill_name'])
      except:
        s_list = None
      
      job_data = {
          'id': job.pk,
          'title': job.title,
          'company': job.company.company_name,
          'location': job.location,
          'status': job.status,
          'qualifications': q_list,
          'skills': s_list
        }
      return JsonResponse(job_data, content_type='application/json')
    except Job.DoesNotExist:
      return JsonResponse({'error': 'Job not found'}, status=404)
  else:
    return JsonResponse({'error': 'Invalid request method'}, status=400)