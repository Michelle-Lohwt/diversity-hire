from django.contrib import admin
from .models import Skill, CandidateSkill

class CandidateSkillAdmin(admin.ModelAdmin):
  list_display = ('candidate', 'skill')

# Register your models here.
admin.site.register(Skill)
admin.site.register(CandidateSkill, CandidateSkillAdmin)