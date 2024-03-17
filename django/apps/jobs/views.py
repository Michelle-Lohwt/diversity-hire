from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..accounts.models import Recruiter
from .models import Job
from .forms import JobForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def create_job(request, pk):
  # ToDo (high): remove recruiter, can login instead (check all request.user)
  recruiter = Recruiter.objects.get(id=pk)
  request.user = recruiter
  # until here end----------------
  request.user.id = pk
  
  form = JobForm()
  
  if request.method == 'POST':
    form = JobForm(request.POST)
    
    if form.is_valid():
      form.instance.created_by = request.user
      form.save()
      return redirect('/recruiter/' + pk + '/dashboard/')
  
  context = {'form': form}
  return render(request, 'jobs/job_form.html', context)

def update_job(request, pk, job_id):
  # ToDo (high): remove recruiter, can login instead (check all request.user)
  recruiter = Recruiter.objects.get(id=pk)
  request.user = recruiter
  # until here end----------------
  request.user.id = pk
  
  job = Job.objects.get(id=job_id)
  request.session['job_id'] = job_id
  
  form = JobForm(instance=job)
  change_job_status = True
  job_status = job.status
  
  if request.method == 'POST':
    form = JobForm(request.POST, instance=job)
    
    if form.is_valid():
      # form.instance.created_by = request.user
      form.save()
      return redirect('/recruiter/' + pk + '/dashboard/')
  
  context = {'form': form, 'change_job_status': change_job_status, 'job_status': job_status}
  return render(request, 'jobs/job_form.html', context)

def change_job_status(request, job_id):
  job = Job.objects.get(id=job_id)
  if job.status == 'Open':
    job.status = "Close"
  else:
    job.status = "Open"
  job.save()
  return HttpResponse(status=200)