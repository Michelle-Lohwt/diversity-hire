from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ChoiceField, TextInput, PasswordInput, Select
from .models import BaseAccount

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