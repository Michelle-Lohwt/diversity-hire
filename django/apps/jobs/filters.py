from django_filters import FilterSet, DateFilter, CharFilter, ChoiceFilter, ModelChoiceFilter, DateFromToRangeFilter
from django.forms import TextInput, Select, DateInput
from ..accounts.models import Company
from .models import Job, JobType, ExperienceType

class JobFilter(FilterSet):
  closing_date_start = DateFilter(field_name='closing_date', lookup_expr='gte',
                                  widget=DateInput(
                                    attrs ={
                                      "type": "date",
                                      "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                                  }))
  closing_date_end = DateFilter(field_name='closing_date', lookup_expr='lte',
                                  widget=DateInput(
                                    attrs ={
                                      "type": "date",
                                      "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                                  }))
  title = CharFilter(field_name='title', lookup_expr='icontains',
                      widget=TextInput(
                       attrs = {
                          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                      }))
  job_type = ChoiceFilter(choices = JobType.choices,
                          widget = Select(
                            attrs = {
                              "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                          }))
  job_required_experience_type = ChoiceFilter(choices = ExperienceType.choices,
                          widget = Select(
                            attrs = {
                              "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                          }))
  company = ModelChoiceFilter(queryset = Company.objects.all(),
                     widget=Select(
                       attrs = {
                          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    }))
  location = CharFilter(field_name='location', lookup_expr='icontains',
                      widget=TextInput(
                       attrs = {
                          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                      }))
  status = ChoiceFilter(choices = Job.JOB_STATUS,
                     widget=Select(
                       attrs = {
                          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                    }))
  class Meta:
    model = Job
    fields = '__all__'
    exclude = ('created_by', 
               'description',
               'closing_date',
               'job_required_qualifications', 
               'job_required_skills',
               'created_at', 
               'modified_at')