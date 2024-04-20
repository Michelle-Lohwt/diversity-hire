from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Job, JobApplication, SkillSimilarities, InterviewScoring, Scorecard
from .forms import JobForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from ..accounts.decorators import allowed_users
from django.db.models import Case, When, Value, IntegerField, Subquery, OuterRef
from ..api.views import (update_skill_matching, 
                         update_qualification_matching,
                         calculate_qualification_matching, 
                         calculate_interview_overall_score,
                         calculate_scorecard_overall_score)

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
      update_qualification_matching(job = job)
      return redirect('/recruiter/dashboard/')
  
  context = {'form': form, 'change_job_status': change_job_status, 'job_status': job_status}
  return render(request, 'jobs/job_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def recruiter_job(request, job_id):
  job = Job.objects.get(pk = job_id)
  applications = JobApplication.objects.filter(job = job, status = 'Applied').annotate(
    overall_score=Subquery(
        Scorecard.objects.filter(application=OuterRef('pk'))
        .values('overall_score')[:1]
    ),
    overall_score_order=Case(
        When(overall_score=None, then=Value(0)),
        default='overall_score',
        output_field=IntegerField(),
    )
).order_by('-overall_score_order')
  
  context = {
    'job': job,
    'applications': applications,
  }
  
  return render(request, 'accounts/recruiter/job.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def recruiter_screening_job(request, job_id):
  job = Job.objects.get(pk = job_id)
  applications = JobApplication.objects.filter(job = job, status = 'Screening').annotate(
    overall_score=Subquery(
        Scorecard.objects.filter(application=OuterRef('pk'))
        .values('overall_score')[:1]
    ),
    overall_score_order=Case(
        When(overall_score=None, then=Value(0)),
        default='overall_score',
        output_field=IntegerField(),
    )
).order_by('-overall_score_order')
  
  context = {
    'job': job,
    'applications': applications,
  }
  
  return render(request, 'accounts/recruiter/job.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def recruiter_interview_job(request, job_id):
  job = Job.objects.get(pk = job_id)
  applications = JobApplication.objects.filter(job = job, status = 'Interview').annotate(
    overall_score=Subquery(
        Scorecard.objects.filter(application=OuterRef('pk'))
        .values('overall_score')[:1]
    ),
    overall_score_order=Case(
        When(overall_score=None, then=Value(0)),
        default='overall_score',
        output_field=IntegerField(),
    )
).order_by('-overall_score_order')
  
  context = {
    'job': job,
    'applications': applications,
  }
  
  return render(request, 'accounts/recruiter/job.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def recruiter_accepted_job(request, job_id):
  job = Job.objects.get(pk = job_id)
  applications = JobApplication.objects.filter(job = job, status = 'Accepted').annotate(
    overall_score=Subquery(
        Scorecard.objects.filter(application=OuterRef('pk'))
        .values('overall_score')[:1]
    ),
    overall_score_order=Case(
        When(overall_score=None, then=Value(0)),
        default='overall_score',
        output_field=IntegerField(),
    )
).order_by('-overall_score_order')
  
  context = {
    'job': job,
    'applications': applications,
  }
  
  return render(request, 'accounts/recruiter/job.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def recruiter_rejected_job(request, job_id):
  job = Job.objects.get(pk = job_id)
  applications = JobApplication.objects.filter(job = job, status = 'Rejected').annotate(
    overall_score=Subquery(
        Scorecard.objects.filter(application=OuterRef('pk'))
        .values('overall_score')[:1]
    ),
    overall_score_order=Case(
        When(overall_score=None, then=Value(0)),
        default='overall_score',
        output_field=IntegerField(),
    )
).order_by('-overall_score_order')
  
  context = {
    'job': job,
    'applications': applications,
  }
  
  return render(request, 'accounts/recruiter/job.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Candidate'])
def candidate_applied_applications(request):
  candidate = request.user.candidate_profile
  applications = candidate.jobApplication_applied_by_candidate.filter(status='Applied')
  
  context = {
    'page_obj': applications,
  }
  return render(request, 'applications/all_applications.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Candidate'])
def candidate_screening_applications(request):
  candidate = request.user.candidate_profile
  applications = candidate.jobApplication_applied_by_candidate.filter(status='Screening')
  
  context = {
    'page_obj': applications,
  }
  return render(request, 'applications/all_applications.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Candidate'])
def candidate_interview_applications(request):
  candidate = request.user.candidate_profile
  applications = candidate.jobApplication_applied_by_candidate.filter(status='Interview')
  
  context = {
    'page_obj': applications,
  }
  return render(request, 'applications/all_applications.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Candidate'])
def candidate_accepted_applications(request):
  candidate = request.user.candidate_profile
  applications = candidate.jobApplication_applied_by_candidate.filter(status='Accepted')
  
  context = {
    'page_obj': applications,
  }
  return render(request, 'applications/all_applications.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Candidate'])
def candidate_rejected_applications(request):
  candidate = request.user.candidate_profile
  applications = candidate.jobApplication_applied_by_candidate.filter(status='Rejected')
  
  context = {
    'page_obj': applications,
  }
  return render(request, 'applications/all_applications.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter', 'Candidate'])
def view_application(request, job_application_id):
  application = JobApplication.objects.get(pk = job_application_id)
  candidate = application.candidate
  job = application.job
  scorecard = application.application_scorecard
  
  qualifications = candidate.qualification_belongs_to_candidate.all()
  skills = candidate.skill_belongs_to_candidate.all()
  experiences = candidate.experience_belongs_to_candidate.all()
  
  context = {
    'candidate': candidate,
    'application': application,
    'scorecard': scorecard,
    'qualifications': qualifications,
    'skills': skills,
    'experiences': experiences,
    'job': job,
  }
  return render(request, 'applications/one_application.html', context)

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
@allowed_users(allowed_roles=['Recruiter'])
def update_application_status(request, application_id):
  pass

@login_required(login_url='login')
@allowed_users(allowed_roles=['Candidate'])
def apply_job(request, job_id):
  candidate = request.user.candidate_profile
  job = Job.objects.get(pk = job_id)
  
  job_application, job_application_created = JobApplication.objects.get_or_create(
    candidate = candidate,
    job = job
  )
  skill_score_obj = SkillSimilarities.objects.get(job = job, candidate = candidate)
  
  interview_score_obj, interview_score_created = InterviewScoring.objects.get_or_create(
    application = job_application
  )
  interview_score_obj.overall_score = calculate_interview_overall_score(interview_score_obj)
  interview_score_obj.save()
  
  scorecard_obj, scorecard_created = Scorecard.objects.get_or_create(
      application = job_application,
      skill_score = skill_score_obj,
      interview_score = interview_score_obj
  )
  scorecard_obj.qualification_score = calculate_qualification_matching(candidate, job)
  scorecard_obj.overall_score = calculate_scorecard_overall_score(scorecard_obj)
  scorecard_obj.save()

  return JsonResponse({'job_application_id': job_application.pk}, content_type='application/json')