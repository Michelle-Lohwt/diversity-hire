from apps.accounts.models import BaseAccount, Recruiter
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
import csv

def run():
  with open('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/recruiter/base_account.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      hashed_password = make_password(row['password'])
      user = BaseAccount.objects.create(
        username = row['username'],
        name = row['name'],
        role = row['role'],
        password = hashed_password
      )
      group, created = Group.objects.get_or_create(name=row['role'])
      if created:
        # New group created, add user directly
        group.user_set.add(user)
      else:
        # Existing group, check if user already belongs
        if user not in group.user_set.all():
            group.user_set.add(user)
      
  with open('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/recruiter/profile.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      user_pk = BaseAccount.objects.get(username = row['user'])
      Recruiter.objects.create(
        user = user_pk,
        gender = row['gender'],
        contact_number = row['contact_number'],
        date_of_birth = row['date_of_birth'],
        recruiter_title = row['recruiter_title'],
        recruiter_summary = row['recruiter_summary'],
        linkedIn_URL = row['linkedIn_URL']
      )