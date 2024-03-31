from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users
from .forms import (
  RegistrationForm, CandidateProfileForm, RecruiterProfileForm, 
  ExperienceFormSet, QualificationFormSet, SkillFormSet
  )
from ..api.views import update_skill_matching
from .models import BaseAccount, Candidate, Recruiter
from ..jobs.models import Job, JobApplication
from ..jobs.filters import JobFilter
import pandas as pd
from gensim.models import Word2Vec
from collections import defaultdict

def home(request):
  return render(request, 'home.html')

@unauthenticated_user
def register(request):
  form = RegistrationForm()
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data['username']
      role = form.cleaned_data['role']
      
      group, created = Group.objects.get_or_create(name=role)
      user.groups.add(group)
      
      if role == 'Recruiter':
        Recruiter.objects.create(user=user)
      elif role == 'Candidate':
        Candidate.objects.create(user=user)
      
      messages.success(request, 'Account was created for ' + role + ' ' + username)
      return redirect('/login/')
  context = {'form': form}
  return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(request, username = username, password = password)
    
    if user is not None:
      login(request, user)
      account = BaseAccount.objects.get(username=username)
      role = account.role
      
      if role == 'Recruiter':
        return redirect('/recruiter/dashboard')
      elif role == 'Candidate':
        return redirect('/candidate/dashboard')
      
    else:
      messages.info(request, 'Username or Password is incorrect')
      return render(request, 'accounts/login.html')
    
  return render(request, 'accounts/login.html')

def logoutUser(request):
  logout(request)
  return redirect('/login/')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def recruiter_dashboard(request):
  print('**************')
  print('Recruiter')
  print(request.user.recruiter_profile)
  print(request.user.recruiter_profile.id)
  print('**************')
  jobs = request.user.recruiter_profile.job_created_by_recruiter.all().order_by('-created_at')
  
  query_dict = request.GET
  filtered_dict = {key: value for key, value in query_dict.items() if value}
  filter = JobFilter(filtered_dict, queryset=jobs)
  jobs = filter.qs
  
  p = Paginator(jobs, 10)
  page_number = request.GET.get('page', 1)
  
  try:
    page_job = p.get_page(page_number)
  except PageNotAnInteger:
    page_job = p.page(1)
  except EmptyPage:
    page_job = p.page(p.num_pages)
    
  # selected_job_obj = page_job[0]
  if not jobs:
    selected_job_obj = None
    select = False
  else:
    selected_job_obj = page_job[0]
    select = True
    
  applications = JobApplication.objects.all()
  
  # ToDo (high): change 
  # request.session['job_id'] = selected_job_obj.pk
  total_jobs = jobs.count()
  
  # total_applications = applications.count()
  # applied = applications.filter('Applied').count()
  # screening = applications.filter('Screening').count()
  # interview = applications.filter('Interview').count()
  # accepted = applications.filter('Accepted').count()
  # rejected = applications.filter('Rejected').count()
  
  context = {
    'recruiter': request.user.recruiter_profile,
    'page_obj': page_job, 
    'filter_query': filtered_dict,
    'filter': filter,
    'select': select,
    'selected_job_obj': selected_job_obj,
    'applications': applications,
    'total_jobs': total_jobs,
  }
  return render(request, 'accounts/recruiter/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter'])
def recruiter_jobs(request, job_id = None):
  jobs = request.user.recruiter_profile.job_created_by_recruiter.all()
  
  # if job_id == None:
  #   jobs = jobs.first()
  # else:
  #   jobs = jobs.filter(job_id)
  
  return render(request, 'accounts/recruiter/jobs.html')

# def recruiter_candidates(request):
#   return render(request, 'accounts/recruiter/dashboard.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Candidate'])
def candidate_dashboard(request):
  print('**************')
  print('Candidate')
  print(request.user.candidate_profile)
  print(request.user.candidate_profile.id)
  print('**************')
  candidate = request.user.candidate_profile
  candidate_skills = candidate.skill_belongs_to_candidate.all()
  
  jobs = candidate.candidate_skill_match.filter(job__status='Open').order_by('-score')
  
  p = Paginator(jobs, 10)
  page_number = request.GET.get('page', 1)
  
  try:
    page_job = p.get_page(page_number)
  except PageNotAnInteger:
    page_job = p.page(1)
  except EmptyPage:
    page_job = p.page(p.num_pages)
    
  selected_job_obj = (page_job[0]).job
  total_jobs = jobs.count()
  
  # recommended_jobs = recommend_jobs(candidate_skills, job_data)
  
  # recommend_words = {}
  # for skill in candidate_skills:
  #   s = str(skill.skill).lower()
  #   try:
  #     for w, sim in skill_model.wv.most_similar(s, topn=3):
  #       recommend_words[w] = sim
  #   except:
  #     pass
  # for title in recommend_words.keys():
  #   filter = JobFilter({'job_required_skills': title}, queryset=jobs)
  #   print(len(filter.qs))
  
  # ToDo (medium): check whether to include the application that candidates
  #                 apply in the candidate dashboard
  # applications = candidate.jobApplication_applied_by_candidate.all()
  context = {
    'page_obj': page_job,
    'selected_job_obj': selected_job_obj,
    'total_jobs': total_jobs,
  }
  return render(request, 'accounts/candidate/dashboard.html', context)
  

@login_required(login_url='login')
@allowed_users(allowed_roles=['Recruiter', 'Candidate'])
def update_profile(request):
  if request.user.role == 'Recruiter':
    is_recruiter = True
    recruiter = request.user.recruiter_profile
    profile_form = RecruiterProfileForm(instance=recruiter)
    
    if request.method == 'POST':
      profile_form = RecruiterProfileForm(request.POST, instance=recruiter)
      
      if profile_form.is_valid():
        profile_form.save()
        return redirect('recruiter-dashboard')
    
    context = {
      'is_recruiter': is_recruiter,
      'form': profile_form, 
    }
  elif request.user.role == 'Candidate':
    is_recruiter = False
    candidate = request.user.candidate_profile
    
    profile_form = CandidateProfileForm(instance=candidate)
    experience_form = ExperienceFormSet(instance=candidate)
    qualification_form = QualificationFormSet(instance=candidate)
    skill_form = SkillFormSet(instance=candidate)
    
    if request.method == 'POST':
      if 'profile_sub' in request.POST:
        profile_form = CandidateProfileForm(request.POST, instance=candidate)
        if profile_form.is_valid():
          profile_form.save()
          return redirect('candidate-dashboard')
        
      elif 'experience_sub' in request.POST:
        experience_form = ExperienceFormSet(request.POST, instance=candidate)
        if experience_form.is_valid():
          experience_form.save()
          return redirect('candidate-dashboard')
        
      elif 'qualification_sub' in request.POST:
        qualification_form = QualificationFormSet(request.POST, instance=candidate)
        if qualification_form.is_valid():
          qualification_form.save()
          return redirect('candidate-dashboard')
      
      elif 'skill_sub' in request.POST:
        skill_form = SkillFormSet(request.POST, instance=candidate)
        # print('**********')
        # print(skill_form.data)
        # print(skill_form.errors)
        # print('**********')
        if skill_form.is_valid():
          skill_form.save()
          update_skill_matching(candidates=candidate, one_candidate=True)
          return redirect('candidate-dashboard')
    
    context = {
      'is_recruiter': is_recruiter,
      'form': profile_form, 
      'experience_formset': experience_form,
      'qualification_formset': qualification_form,
      'skill_formset': skill_form,
    }
  return render(request, 'common/account_profile.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['Recruiter', 'Candidate'])
# def view_profile(request):
#   context = {}
#   return render(request, 'common/account_profile.html', context)

# API
def get_job_details(request, job_id):
  if request.method == 'GET':
    try:
      job = Job.objects.get(pk=job_id)
      try:
        q_dict = defaultdict(list)
        for q in job.job_required_qualifications.values():
          q_dict[q['qualification_name']].append(q['qualification_type'])
          
        q_list = []
        for name, types in q_dict.items():
          concatenated_types = '/ '.join(types)  # Join types with comma and space
          q_list.append(concatenated_types + ' in ' + name)
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
          'description': job.description,
          'closing_date': job.closing_date.strftime("%B %d, %Y"),
          'job_type': job.job_type,
          'company': job.company.company_name,
          'location': job.location,
          'status': job.status,
          'experience': job.job_required_experience_type,
          'qualifications': q_list,
          'skills': s_list
        }
      return JsonResponse(job_data, content_type='application/json')
    except Job.DoesNotExist:
      return JsonResponse({'error': 'Job not found'}, status=404)
  else:
    return JsonResponse({'error': 'Invalid request method'}, status=400)