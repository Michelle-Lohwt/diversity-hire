from django.contrib import admin
from .models import Job, JobApplication, SkillSimilarities

class JobAdmin(admin.ModelAdmin):
  list_display = ('title', 'company')
  
class SkillSimilaritiesAdmin(admin.ModelAdmin):
  list_display = ('job', 'candidate', 'score')

# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication)
admin.site.register(SkillSimilarities, SkillSimilaritiesAdmin)