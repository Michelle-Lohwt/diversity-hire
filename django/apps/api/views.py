from django.shortcuts import render
from ..accounts.models import Candidate
from ..jobs.models import Job, SkillSimilarities
from gensim.models import Word2Vec
from django.db import transaction
import time

# Create your views here.

def calculate_skill_matching(candidate_skills, job_skills, skill_model):
  avg_score = 0
  
  for skill in candidate_skills:
    str_skill = str(skill.skill).lower()
    total_score = 0
    for job_skill in job_skills:
      str_job_skill = str(job_skill).lower()
      score = skill_model.wv.similarity(str_skill, str_job_skill)
      total_score += score
    avg_score += (total_score/len(job_skills))
  avg_score /= len(candidate_skills)
  
  return avg_score * 100
      
def update_skill_matching(candidates=Candidate.objects.all(), jobs = Job.objects.filter(status='Open'), one_candidate = False, one_job = False):
  # For demo ---------
  start_time = time.time()
  # ------------------
  skill_model = Word2Vec.load('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/nlp/skill_model')
  
  if one_job:
    # One job only
    job_skills = jobs.job_required_skills.all()
    for candidate in candidates:
      candidate_skills = candidate.skill_belongs_to_candidate.all()
      try:
        score = calculate_skill_matching(candidate_skills, job_skills, skill_model)
      except:
        score = 0
      
      with transaction.atomic():
        obj, created = SkillSimilarities.objects.select_for_update().get_or_create(
          job = jobs,
          candidate = candidate,
          defaults={'score': score}
        )
        if not created:
          obj.score = score
          obj.save()
        
  elif one_candidate:
    # One candidate only
    candidate_skills = candidates.skill_belongs_to_candidate.all()
    count = 0
    for job in jobs:
      job_skills = job.job_required_skills.all()
      try:
        score = calculate_skill_matching(candidate_skills, job_skills, skill_model)
      except:
        score = 0
        
      with transaction.atomic():
        obj, created = SkillSimilarities.objects.select_for_update().get_or_create(
          job = job,
          candidate = candidates,
          defaults={'score': score}
        )
        if not created:
          obj.score = score
          obj.save()
  # For demo ---------
  elapsed_time = time.time() - start_time
  print(elapsed_time)
  # ------------------