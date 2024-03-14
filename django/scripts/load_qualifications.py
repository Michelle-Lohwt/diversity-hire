from apps.qualifications.models import Qualification
import csv

def run():
  with open('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/qualification.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      Qualification.objects.create(
        qualification_type = row['qualification'],
        qualification_name = row['qualification_name']
      )