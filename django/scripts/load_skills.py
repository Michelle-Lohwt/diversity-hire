from apps.skills.models import Skill
import csv

def run():
  with open('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/skill.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      Skill.objects.create(
        skill_name = row['skill_name']
      )