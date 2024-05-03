from django.contrib.auth.forms import UserCreationForm
from django.forms import (ModelForm, 
                          inlineformset_factory,
                          CharField, 
                          ChoiceField, 
                          DateInput, 
                          TextInput, 
                          PasswordInput, 
                          Select, 
                          Textarea, 
                          URLInput)
from .models import BaseAccount, Candidate, Recruiter, Company, Experience
from ..qualifications.models import CandidateQualification
from ..skills.models import CandidateSkill

class RegistrationForm(UserCreationForm):
  password1 = CharField(widget=PasswordInput(
            attrs = {
              "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            }
          ))
  password2 = CharField(widget=PasswordInput(
            attrs = {
              "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            }
          ))
  role = ChoiceField(choices=(
        ('Recruiter', 'Recruiter'),
        ('Candidate', 'Candidate'),
        ), widget=Select(
            attrs = {
              "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            }
          ))
  
  class Meta:
    model = BaseAccount
    fields = ('username', 'name', 'role', 'password1', 'password2')
    widgets = {
        'username': TextInput(
            attrs = {
              "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            }
          ),
        'name': TextInput(
            attrs = {
              "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            }
          ),
        }
    
class CandidateProfileForm(ModelForm):
  class Meta:
    model = Candidate
    fields = ('gender', 'phone_number', 'date_of_birth', 'candidate_summary', 'linkedIn_URL')
    widgets = {
      'candidate_summary': Textarea(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'linkedIn_URL': URLInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'gender': Select(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'phone_number': TextInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'date_of_birth': DateInput(
        attrs={
          "type": "date",
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
    }
    
class RecruiterProfileForm(ModelForm):
  class Meta:
    model = Recruiter
    fields = ('gender', 'contact_number', 'date_of_birth', 'recruiter_title', 'recruiter_summary', 'linkedIn_URL')
    widgets = {
      'recruiter_title': TextInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'recruiter_summary': Textarea(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'linkedIn_URL': URLInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'gender': Select(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'contact_number': TextInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'date_of_birth': DateInput(
        attrs={
          "type": "date",
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
    }
    
class CompanyForm(ModelForm):
  class Meta:
    model = Company
    fields = ('company_name', 'company_description', 'address', 'website_URL', 'industry')
    widgets = {
      'company_name': TextInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'company_description': Textarea(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'address': TextInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'website_URL': URLInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'industry': Select(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
    }
    
class ExperienceForm(ModelForm):
  class Meta:
    model = Experience
    fields= ('job_title', 'job_description', 'company_name', 'start_date', 'end_date')
    widgets = {
      'job_title': TextInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'job_description': Textarea(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'company_name': TextInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'start_date': DateInput(
        attrs={
          "type": "date",
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'end_date': DateInput(
        attrs={
          "type": "date",
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
    }
    
class CandidateQualificationForm(ModelForm):
  class Meta:
    model = CandidateQualification
    fields = ('qualification', 'institue_name', 'qualification_description', 'start_date', 'end_date')
    widgets = {
      'qualification': Select(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'institue_name': TextInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'qualification_description': Textarea(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'start_date': DateInput(
        attrs={
          "type": "date",
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'end_date': DateInput(
        attrs={
          "type": "date",
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
    }
    
class CandidateSkillForm(ModelForm):
  class Meta:
    model = CandidateSkill
    fields = ('skill',)
    widgets = {
      'skill': Select(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
    }
    

# FormSets
ExperienceFormSet = inlineformset_factory(Candidate, Experience, extra=1, can_delete=True, can_delete_extra=True,
                                          fields= ('job_title', 'job_description', 'company_name', 'start_date', 'end_date'),
                                          form=ExperienceForm)
QualificationFormSet = inlineformset_factory(Candidate, CandidateQualification, extra=1, can_delete=True, can_delete_extra=True,
                                          fields= ('qualification', 'institue_name', 'qualification_description', 'start_date', 'end_date'),
                                          form=CandidateQualificationForm)
SkillFormSet = inlineformset_factory(Candidate, CandidateSkill, extra=1, can_delete=True, can_delete_extra=True,
                                          fields= ('skill',),
                                          form=CandidateSkillForm)