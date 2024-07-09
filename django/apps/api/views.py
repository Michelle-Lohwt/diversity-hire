from django.shortcuts import render
from django.conf import settings
from ..accounts.models import Candidate
from ..jobs.models import Job, SkillSimilarities, JobApplication, Scorecard
from gensim.models import Word2Vec
from django.db import transaction
import time
from collections import defaultdict
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.db.models import Q

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
  
  qualification_levels = {'certificate': 1, 'diploma': 2, 'bachelor': 3, 'master': 4, 'phd': 5}
  similarity_scores = []
  
  # Group qualifications by name
  candidate_q_grouped = defaultdict(list)
  for q in candidate_qualifications:
    candidate_q_grouped[q.qualification.qualification_name].append(q.qualification.qualification_type)

  job_q_grouped = defaultdict(list)
  for q in job_qualifications:
    job_q_grouped[q.qualification_name].append(q.qualification_type)
    
  # Iterate through qualification groups and calculate match score
  # Reference: https://g.co/gemini/share/6b6c790212e8
  for job_q_name, job_q_types in job_q_grouped.items():
    
    for candidate_q_name, candidate_q_types in candidate_q_grouped.items():
      similarity = qualification_model.wv.similarity(candidate_q_name.lower(), job_q_name.lower())
      # print('*********')
      # print(job_q_types, candidate_q_types)
      # print(job_q_name, candidate_q_name, similarity)
      # print('*********')
      
      matching_q_types = set(candidate_q_types) & set(job_q_types)
      max_candidate_qualification = candidate_q_types[-1].lower()
      max_candidate_qualification_level = qualification_levels[max_candidate_qualification]
      
      # Case 1: Exact matched
      if ((len(matching_q_types) == candidate_q_types.__len__()) and (len(matching_q_types) == job_q_types.__len__())):
        score_modifier = 1.0
        
      # Case 2: At least one qualification type matched
      if matching_q_types:
        min_matched_qualification = list(matching_q_types)[0].lower()
        min_matched_qualification_level = qualification_levels[min_matched_qualification]
        
        level_diff = max_candidate_qualification_level - min_matched_qualification_level
        # Case 2.1: One matched with higher level
        if level_diff > 0:
          score_modifier = 1.0 + 0.1 * level_diff
        # Case 2.2: One matched
        elif level_diff == 0:
          score_modifier = 1.0
          
      # Case 3: No qualification type matched
      else:
        min_job_qualification = job_q_types[0].lower()
        min_job_qualification_level = qualification_levels[min_job_qualification]
        
        level_diff = abs(max_candidate_qualification_level - min_job_qualification_level)
        
        # Case 3.1: All candidate qualification types are lower than the required job qualification types
        if level_diff < 0:
          score_modifier = 1.0 - 0.1 * level_diff
        # Case 3.2: All candidate qualification types are higher than the required job qualification types
        elif level_diff > 0:
          score_modifier = 1.0 - 0.05 * level_diff
         
      similarity *= score_modifier
      if similarity >= 1.0:
        similarity = 1.0
      # print(score_modifier)
      # print(similarity)
      similarity_scores.append(similarity)
      
  # print(max(similarity_scores))
  return (max(similarity_scores) * 100)

def scrolling(driver):
  start = time.time()
  
  # will be used in the while loop
  initialScroll = 0
  finalScroll = 1000
 
  while True:
    driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
    initialScroll = finalScroll
    finalScroll += 1000
    
    time.sleep(0.2)
    end = time.time()

    if round(end - start) > 10:
      break

def scrapping(url, driver):
  driver.get(url)
  time.sleep(2)
  scrolling(driver)
  page_source = driver.page_source
  soup = BeautifulSoup(page_source, "html.parser")
  recent_posts = soup.find_all("div", class_="feed-shared-update-v2")
  
  content = []
  for post in recent_posts[:100]:
    post_content = post.find("div", class_="feed-shared-update-v2__description")
    if post_content:
      content.append(post_content.get_text().strip())
      
  return content

def remove_unnecessary_characters(text):
    text = re.sub(r'<.*?>', '', str(text))
    text = re.sub(r'[^a-zA-Z0-9\s]', '', str(text))
    text = re.sub(r'\s+', ' ', str(text)).strip()
    return text

def calculate_sentiment_score(candidate):
  # For demo ---------
  start_time = time.time()
  # ------------------
  try:
    chromedriver_path = "C:/Users/WT/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    service = Service(executable_path=chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://linkedin.com/uas/login")
    time.sleep(2)
    
    username = driver.find_element(By.ID, "username")
    username.send_keys(settings.EMAIL)

    pword = driver.find_element(By.ID, "password")
    pword.send_keys(settings.PASSWORD)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    content = scrapping(candidate.linkedIn_URL + '/recent-activity/all/', driver)
    analyzer = SentimentIntensityAnalyzer()
    total_compound_score = 0
    
    for post in content:
      text = remove_unnecessary_characters(post)
      sentiment_score = analyzer.polarity_scores(text)
      total_compound_score += sentiment_score['compound']
    avg_compound_score = total_compound_score/len(content)
  except:
    avg_compound_score = 0
    
  # For demo ---------
  print('*******')
  elapsed_time = time.time() - start_time
  print(elapsed_time)
  print(avg_compound_score)
  print('*******')
  
  # ------------------
  return avg_compound_score * 100

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
    
def update_sentiment_score():
  applications = JobApplication.objects.exclude(Q(status='Accepted') | Q(status='Rejected'))
  for application in applications:
    scorecard = Scorecard.objects.get(application = application)
    scorecard.social_media_score = calculate_sentiment_score(application.candidate)
    scorecard.overall_score = calculate_scorecard_overall_score(scorecard)
    scorecard.save()