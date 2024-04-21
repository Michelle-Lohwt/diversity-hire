from django.forms import ModelForm, TextInput, Textarea, Select, DateInput, SelectMultiple, NumberInput
from .models import Job, InterviewScoring

class JobForm(ModelForm):
  class Meta:
    model = Job
    fields = '__all__'
    exclude = ('created_by', 'status',)
    
    widgets = {
      'title': TextInput(
        attrs = {
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'description': Textarea(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'company': Select(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        }
      ),
      'location': TextInput(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        }
      ),
      'closing_date': DateInput(
        attrs ={
          "type": "date",
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        }
      ),
      'job_type': Select(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        }
      ),
      'job_required_experience_type': Select(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        }
      ),
      'job_required_qualifications': SelectMultiple(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        }
      ),
      'job_required_skills': SelectMultiple(
        attrs={
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        }
      ),
    }
    
class InterviewForm(ModelForm):
  class Meta:
    model = InterviewScoring
    fields = ('intellectual_curious_score',
              'self_motivation_score',
              'articulate_score',
              'analytical_and_product_minded_score',
              'remarks')
    widgets = {
      'intellectual_curious_score': NumberInput(
        attrs = {
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'self_motivation_score': NumberInput(
        attrs = {
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'articulate_score': NumberInput(
        attrs = {
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'analytical_and_product_minded_score': NumberInput(
        attrs = {
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
      'remarks': Textarea(
        attrs = {
          "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        }
      ),
    }