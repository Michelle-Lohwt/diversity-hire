from apps.accounts.models import BaseAccount, Candidate
import csv

def run():
  with open('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/candidate/base_account.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      BaseAccount.objects.create(
        username = row['username'],
        name = row['name'],
        role = row['role'],
        password = row['password']
      )
      
  with open('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/candidate/profile.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      user_pk = BaseAccount.objects.get(username = row['user'])
      Candidate.objects.create(
        user = user_pk,
        gender = row['gender'],
        phone_number = row['phone_number'],
        date_of_birth = row['date_of_birth'],
        candidate_summary = row['candidate_summary'],
        linkedIn_URL = row['linkedIn_URL']
      )