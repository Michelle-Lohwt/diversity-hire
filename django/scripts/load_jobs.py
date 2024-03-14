from apps.jobs.models import Job, Recruiter, Company, Qualification, Skill
import pandas as pd

def create_jobs(quarter, recruiter, companies, jobs_required_qualifications, jobs_required_skills):
  for index, row in quarter.iterrows():
    company_id = companies[companies['company_id'] == row['company_id']]['company_id'].iloc[0]
    
    job = Job.objects.create(
      created_by = recruiter,
      title = row['title'],
      description = row['description'],
      location = row['location'],
      job_type = row['job_type'],
      job_required_experience_type = row['job_required_experience_type'],
      company = Company.objects.get(company_id = company_id),
    )
    
    job_id = row['job_id']
    
    qualification_list = jobs_required_qualifications[jobs_required_qualifications['id'] == job_id]
    for index, qualification in qualification_list.iterrows():
      q = Qualification.objects.get(qualification_type = qualification['qualification'], qualification_name = qualification['qualification_name'])
      job.job_required_qualifications.add(q)
    
    skill_list = jobs_required_skills[jobs_required_skills['job_id'] == job_id]['skill_name']
    for skill in skill_list:
      s = Skill.objects.get(skill_name = skill)
      job.job_required_skills.add(s)

def run():
  jobs = pd.read_csv('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/jobs/jobs.csv')
  jobs_required_qualifications = pd.read_csv('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/jobs/job_required_qualifications_random.csv')
  jobs_required_skills = pd.read_csv('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/jobs/job_required_skills.csv')
  companies = pd.read_csv('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/company.csv')
  
  print(jobs_required_skills.columns)
  print(jobs_required_qualifications.columns)
  
  q1 = jobs.iloc[:5679]
  q2 = jobs.iloc[5679:11358]
  q3 = jobs.iloc[11358:]
  
  recruiter_1 = Recruiter.objects.get(id=1)
  recruiter_2 = Recruiter.objects.get(id=2)
  recruiter_3 = Recruiter.objects.get(id=3)
  
  create_jobs(q1, recruiter_1, companies, jobs_required_qualifications, jobs_required_skills)
  create_jobs(q2, recruiter_2, companies, jobs_required_qualifications, jobs_required_skills)
  create_jobs(q3, recruiter_3, companies, jobs_required_qualifications, jobs_required_skills)