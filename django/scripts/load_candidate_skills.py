from apps.accounts.models import Candidate
from apps.skills.models import CandidateSkill, Skill
from apps.api.views import update_skill_matching
import pandas as pd

def run():
  skills = pd.read_csv('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/candidate_skills_random.csv')
  for index, row in skills.iterrows():
    s = Skill.objects.get(skill_name = row['skill'])
    c = Candidate.objects.get(user__username = row['candidate_id'])
    CandidateSkill.objects.get_or_create(candidate = c, skill = s)
    
  candidates = Candidate.objects.all()
  # count = 0
  for candidate in candidates:
    update_skill_matching(candidates=candidate, one_candidate=True)
    # count += 1
    # print(count)