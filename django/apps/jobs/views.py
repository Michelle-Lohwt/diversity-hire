from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Job, JobApplication
from .forms import JobForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from ..accounts.decorators import allowed_users
from ..api.views import update_skill_matching


def jobs(request):
  jobs = Job.objects.all()
  
  p = Paginator(jobs, 20)
  page_number = request.GET.get('page')
  
  try:
    page_obj = p.get_page(page_number)
  except PageNotAnInteger:
    page_obj = p.page(1)
  except EmptyPage:
    page_obj = p.page(p.num_pages)
    
  return render(request, 'jobs/all_jobs.html', {'page_obj': page_obj})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def create_job(request):
  form = JobForm()
  
  if request.method == 'POST':
    form = JobForm(request.POST)
    
    if form.is_valid():
      form.instance.created_by = request.user.recruiter_profile
      form.save()
      return redirect('/recruiter/dashboard/')
  
  context = {'form': form}
  return render(request, 'jobs/job_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def update_job(request, job_id):
  job = Job.objects.get(id=job_id)
  request.session['job_id'] = job_id
  
  form = JobForm(instance=job)
  change_job_status = True
  job_status = job.status
  
  if request.method == 'POST':
    form = JobForm(request.POST, instance=job)
    
    if form.is_valid():
      form.save()
      update_skill_matching(jobs=job, one_job=True)
      return redirect('/recruiter/dashboard/')
  
  context = {'form': form, 'change_job_status': change_job_status, 'job_status': job_status}
  return render(request, 'jobs/job_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Candidate'])
def view_application(request, job_application_id):
  candidate = request.user.candidate_profile
  application = JobApplication.objects.get(pk = job_application_id)
  job = application.job
  
  qualifications = candidate.qualification_belongs_to_candidate.all()
  skills = candidate.skill_belongs_to_candidate.all()
  experiences = candidate.experience_belongs_to_candidate.all()
  
  context = {
    'candidate': candidate,
    'application': application,
    'qualifications': qualifications,
    'skills': skills,
    'experiences': experiences,
    'selected_job_obj': job,
  }
  return render(request, 'common/one_application.html', context)

# API
@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def change_job_status(request, job_id):
  job = Job.objects.get(id=job_id)
  if job.status == 'Open':
    job.status = "Close"
  else:
    job.status = "Open"
    update_skill_matching(jobs=job, one_job=True)
  job.save()
  return HttpResponse(status=200)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Candidate'])
def apply_job(request, job_id):
  candidate = request.user.candidate_profile
  job = Job.objects.get(pk = job_id)
  
  job_application, created = JobApplication.objects.get_or_create(
    candidate = candidate,
    job = job
  )

  return JsonResponse({'job_application_id': job_application.pk}, content_type='application/json')