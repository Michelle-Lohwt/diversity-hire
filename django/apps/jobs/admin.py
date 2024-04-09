from django.contrib import admin
from .models import Job, JobApplication, SkillSimilarities

class JobAdmin(admin.ModelAdmin):
  list_display = ('title', 'company')
  
class JobApplicationAdmin(admin.ModelAdmin):
  list_display = ('job', 'candidate', 'status')
  
class SkillSimilaritiesAdmin(admin.ModelAdmin):
  list_display = ('job', 'candidate', 'score')

# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(SkillSimilarities, SkillSimilaritiesAdmin)