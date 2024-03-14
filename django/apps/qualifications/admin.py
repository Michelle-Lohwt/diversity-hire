from django.contrib import admin
from .models import Qualification, CandidateQualification

# Register your models here.
admin.site.register(Qualification)
admin.site.register(CandidateQualification)