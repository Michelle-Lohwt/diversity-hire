from django.contrib import admin
from .models import (
  BaseAccount, 
  Candidate, 
  Experience,
  Recruiter,
  Company,
  )

class CompanyAdmin(admin.ModelAdmin):
  list_display = ('company_name', 'industry')
  
class BaseAccountAdmin(admin.ModelAdmin):
  list_display = ('name', 'role')
  
class RecruiterAdmin(admin.ModelAdmin):
  list_display = ('user', 'recruiter_title')
  
class ExperienceAdmin(admin.ModelAdmin):
  list_display = ('job_title', 'candidate')

# Register your models here.
admin.site.register(BaseAccount, BaseAccountAdmin)

admin.site.register(Candidate)
admin.site.register(Experience, ExperienceAdmin)

admin.site.register(Recruiter, RecruiterAdmin)

admin.site.register(Company, CompanyAdmin)