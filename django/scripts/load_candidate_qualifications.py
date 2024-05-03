from apps.accounts.models import Candidate
from apps.qualifications.models import Qualification, CandidateQualification
import pandas as pd
from datetime import datetime

def run():
  qualifications = pd.read_csv('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/candidate_qualification.csv')
  for index, row in qualifications.iterrows():
    q = Qualification.objects.get(qualification_type=row['level'], qualification_name=row['major'])
    c = Candidate.objects.get(user__username = row['id'])
    try:
      start_date = datetime.strptime(str(row['start_year']).replace('.0', ''), '%Y').date()
      end_date = datetime.strptime(str(row['end_year']).replace('.0', ''), '%Y').date()
    except:
      start_date = None
      end_date = None
    
    if start_date and end_date:
      CandidateQualification.objects.get_or_create(
        candidate = c,
        qualification = q,
        institue_name = row['institution'],
        qualification_description = row['description'],
        start_date = start_date,
        end_date = end_date
      )
    else:
      CandidateQualification.objects.get_or_create(
        candidate = c,
        qualification = q,
        institue_name = row['institution'],
        qualification_description = row['description'],
      )