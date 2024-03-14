from django.contrib import admin
from .models import Job, JobApplication

class JobAdmin(admin.ModelAdmin):
  list_display = ('title', 'company')

# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication)