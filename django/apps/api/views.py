from django.shortcuts import render
from ..accounts.models import Candidate
from ..jobs.models import Job, SkillSimilarities, JobApplication, Scorecard
from gensim.models import Word2Vec
from django.db import transaction
import time
from collections import defaultdict
from decimal import Decimal

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
  
def calculate_qualification_matching(candidate, job):
  qualification_model = Word2Vec.load('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/nlp/qualification_model')
  
  candidate_qualifications = candidate.qualification_belongs_to_candidate.all()
  job_qualifications = job.job_required_qualifications.all()
  
  candidate_q_dict = defaultdict(list)
  for q in candidate_qualifications:
    candidate_q_dict[q.qualification.qualification_type].append(q.qualification.qualification_name)
  
  job_q_dict = defaultdict(list)
  for q in job_qualifications:
    job_q_dict[q.qualification_type].append(q.qualification_name)
  
  result = {}
  max_similarity = 0
  candidate_q_type = None
  for q_type in set(job_q_dict.keys()):
    job_qualifications = [q.lower() for q in job_q_dict[q_type]]
    candidate_qualifications = [q.lower() for q in candidate_q_dict.get(q_type, [])]
    qualification_types = ['certificate', 'diploma', 'bachelor', 'master', 'phd']

    for candidate_q in candidate_qualifications:
      for job_q in job_qualifications:
        similarity = qualification_model.wv.similarity(candidate_q, job_q)
        if similarity > max_similarity:
          max_similarity = similarity
          candidate_q_type = q_type

    if candidate_q_type:
      candidate_q_index = qualification_types.index(candidate_q_type.lower())
      job_q_index = qualification_types.index(q_type.lower())
      if candidate_q_index > job_q_index:
          max_similarity *= 1.2  # Increase the similarity score by 20%
      elif candidate_q_index < job_q_index:
          max_similarity *= 0.8  # Decrease the similarity score by 20%
      result[q_type] = (candidate_q_type, max_similarity)
    else:
      result[q_type] = ("Unknown", 0.0)

  # Get the maximum similarity score across all job_required_qualification types
  max_score = max(score for _, score in result.values())
  result = {q_type: (candidate_q_type, score) for q_type, (candidate_q_type, score) in result.items() if score == max_score}
  
  final_score = list(result.values())[0][1] * 100
  
  if final_score > 100:
    return 100
  elif final_score < 0:
    return 0
  else:
    return final_score

def calculate_scorecard_overall_score(instance):
  score = (instance.skill_score.score + 
          (Decimal(instance.qualification_score)) + 
          (Decimal(instance.social_media_score)) + 
          instance.interview_score.overall_score) / 4
  return score

def calculate_interview_overall_score(instance):
  score = ((Decimal(instance.intellectual_curious_score)) + 
            (Decimal(instance.self_motivation_score)) + 
            (Decimal(instance.articulate_score)) + 
            (Decimal(instance.analytical_and_product_minded_score))) / 4
  return score

def update_qualification_matching(job):
  applications = JobApplication.objects.filter(job = job)
  for application in applications:
    scorecard = Scorecard.objects.get(application = application)
    scorecard.qualification_score = calculate_qualification_matching(application.candidate, job)
    scorecard.overall_score = calculate_scorecard_overall_score(scorecard)
    scorecard.save()