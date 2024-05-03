from apps.accounts.models import BaseAccount, Candidate
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
import csv
import random

def run():
  with open('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/candidate.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      hashed_password = make_password('abc123_dh')
      user = BaseAccount.objects.create(
        username = row['id'],
        name = row['name'],
        role = 'Candidate',
        password = hashed_password
      )
      group, created = Group.objects.get_or_create(name='Candidate')
      if created:
        # New group created, add user directly
        group.user_set.add(user)
      else:
        # Existing group, check if user already belongs
        if user not in group.user_set.all():
            group.user_set.add(user)
      
      candidate = Candidate.objects.create(
        user = user,
        gender = random.choice(['Male', 'Female']),
        phone_number = '123456789',
        date_of_birth = '2024-03-13',
        candidate_summary = row['about'],
        linkedIn_URL = row['url']
      )