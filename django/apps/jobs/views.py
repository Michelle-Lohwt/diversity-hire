from django.shortcuts import render
from .models import Job
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
