from django.contrib import admin
from .models import Job, JobApplication, SkillSimilarities, InterviewScoring, Scorecard

class JobAdmin(admin.ModelAdmin):
  list_display = ('title', 'company')
  
class JobApplicationAdmin(admin.ModelAdmin):
  list_display = ('job', 'candidate', 'status')
  
class SkillSimilaritiesAdmin(admin.ModelAdmin):
  list_display = ('job', 'candidate', 'score')
  
class InterviewScoringAdmin(admin.ModelAdmin):
  list_display = ('application', 'overall_score')
  
class ScorecardAdmin(admin.ModelAdmin):
  list_display = ('application', 'skill_score', 'qualification_score', 'social_media_score', 'interview_score', 'overall_score')

# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(SkillSimilarities, SkillSimilaritiesAdmin)
admin.site.register(InterviewScoring, InterviewScoringAdmin)
admin.site.register(Scorecard, ScorecardAdmin)