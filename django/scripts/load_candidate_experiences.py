from apps.accounts.models import Candidate, Experience
import pandas as pd
from datetime import datetime


def run():
  experiences = pd.read_csv('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/candidate_experience_1.csv')
  # Experience.objects.all().delete()
  for index, row in experiences.iterrows():
    c = Candidate.objects.get(user__username = row['id'])
    if row['description'] == 'nan':
      row['description'] = None
    if row['company'] == 'nan':
      row['company'] = None
      
    try:
      start_date = datetime.strptime(str(row['start_date']).replace('.0', ''), '%Y').date()
      end_date = datetime.strptime(str(row['end_date']).replace('.0', ''), '%Y').date()
    except:
      start_date = None
      end_date = None
    
    Experience.objects.get_or_create(
      candidate = c,
      job_title = row['title'],
      job_description = row['description'],
      company_name = row['company'],
      start_date = start_date,
      end_date = end_date
    )