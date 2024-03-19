from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import RegistrationForm
from .models import BaseAccount, Candidate, Recruiter
from ..jobs.models import Job, JobApplication
from ..jobs.filters import JobFilter

def home(request):
  return render(request, 'home.html')

def register(request):
  form = RegistrationForm()
  
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      role = form.cleaned_data['role']
      
      user = BaseAccount.objects.get(username=username)
      group, created = Group.objects.get_or_create(name=role)
      if created:
        # New group created, add user directly
        group.user_set.add(user)
      else:
        # Existing group, check if user already belongs
        if user not in group.user_set.all():
            group.user_set.add(user)
      # group = Group.objects.get_or_create(name=role)
      # group.user_set.add(user)
      
      if role == 'Recruiter':
        profile = Recruiter()
        profile.user = user
        profile.save()
      elif role == 'Candidate':
        profile = Candidate()
        profile.user = user
        profile.save()
      
      messages.success(request, 'Account was created for ' + role + ' ' + username)
      return redirect('/login/')
  
  context = {'form': form}
  return render(request, 'accounts/register.html', context)

def loginPage(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    # request.user.id = account.pk
    print('*************')
    print('*************')
    print(username)
    print(password)
    # TODO(HIGH): login accounts that are populated from csv
    user = authenticate(request, username = username, password = password)
    
    if user is not None:
      login(request, user)
      account = BaseAccount.objects.get(username=username)
      role = account.role
      
      if role == 'Recruiter':
        recruiter, created = Recruiter.objects.get_or_create(user=account)
        print('************')
        print('Recruiter' + created)
        print('************')
        return redirect('/recruiter/' + str(request.user.recruiter_profile.id) + '/dashboard')
      elif role == 'Candidate':
        candidate, created = Candidate.objects.get_or_create(user=account)
        print('************')
        print('Candidate' + created)
        print('************')
        return redirect('/candidate/' + str(request.user.candidate_profile.id) + '/dashboard')
      
    else:
      messages.info(request, 'Username or Password is incorrect')
      return render(request, 'accounts/login.html')
    
  return render(request, 'accounts/login.html')

def logoutUser(request):
  logout(request)
  return redirect('/logout/')

def recruiter_dashboard(request, pk):
  print('**************')
  print('Recruiter')
  print(pk)
  print(request.user.recruiter_profile)
  print(request.user.recruiter_profile.id)
  print('**************')
  recruiter = Recruiter.objects.get(id=pk)
  jobs = Job.objects.filter(created_by = recruiter)
  
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
    selected_job_obj = jobs[0]
    select = True
    
  applications = JobApplication.objects.all()
  
  request.user.id = pk
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
    'recruiter': recruiter,
    'page_obj': page_job, 
    'filter_query': filtered_dict,
    'filter': filter,
    'select': select,
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

def candidate_dashboard(request, pk):
  print('**************')
  print('Candidate')
  print(pk)
  print(request.user.candidate_profile)
  print(request.user.candidate_profile.id)
  print('**************')
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