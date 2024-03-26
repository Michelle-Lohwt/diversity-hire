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
from .models import BaseAccount, Candidate, Recruiter
from ..jobs.models import Job, JobApplication
from ..jobs.filters import JobFilter

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
  jobs = request.user.recruiter_profile.job_created_by_recruiter.all()
  
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
  jobs = Job.objects.all()
  applications = request.user.candidate_profile.jobApplication_applied_by_candidate.all()
  return render(request, 'accounts/candidate/dashboard.html')
  

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
  
# class CandidateProfileInline():
#   form_class = CandidateProfileForm
#   model = Candidate
#   template_name = 'common/account_profile.html'
  
#   def form_valid(self, form):
#     pass
    
#   def formset_experience_valid(self, formset):
#     experiences = formset.save(commit=False)
#     for obj in formset.deleted_objects:
#       obj.delete()
#     for experience in experiences:
#       experience.candidate = self.object
#       experience.save()
    
# class CandidateProfileUpdate(CandidateProfileInline, UpdateView):
#   def get_context_data(self, **kwargs):
#     ctx = super(CandidateProfileUpdate, self).get_context_data(**kwargs)
#     print(ctx)
#     # ctx['named_formsets'] = self.get_named_formsets()
#     # return ctx
  
#   def get_named_formsets(self):
#     return{
#       'experiences': ExperienceFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='experiences'),
#     }
    
# def delete_experience(request, exp_id):
#   try:
#     exp = Experience.objects.get(id = exp_id)
#   except Experience.DoesNotExist:
#     messages.success(
#       request, 'Object does not exists.'
#     )
#     return redirect('profiles:update_profile', pk=exp.candidate.id)
#   exp.delete()
#   messages.success(request, 'Experience deleted successfully')
#   return redirect('profiles:update_profile', pk=exp.candidate.id)