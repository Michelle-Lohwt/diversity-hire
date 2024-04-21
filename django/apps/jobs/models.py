from datetime import *
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ..accounts.models import Candidate, Recruiter, Company
from ..qualifications.models import Qualification
from ..skills.models import Skill

def return_date_time():
  now = datetime.now()
  return now + timedelta(days=60)

class JobType(models.TextChoices):
  Full_Time = "Full-time"
  Contract = "Contract"
  Part_Time = "Part-time"
  Volunteer = "Volunteer"
  Temporary = "Temporary"
  Internship = "Internship"
  Other = "Other"
  
class ExperienceType(models.TextChoices):
  Internship = 'Internship'
  Entry = 'Entry Level'
  Associate = 'Associate'
  Mid_Senior = 'Mid-Senior Level'
  Director = 'Director'
  Executive = 'Executive'

class Job(models.Model):
  JOB_STATUS = (
    ('Open', 'Open'),
    ('Close', 'Close'),
  )
  created_by = models.ForeignKey(Recruiter, on_delete=models.SET_NULL, null=True, related_name='job_created_by_recruiter')
  
  title = models.CharField(max_length=255, null=True)
  description = models.TextField(null=True)
  location = models.CharField(max_length=255, null=True)
  closing_date = models.DateField(default=return_date_time)
  status = models.CharField(max_length = 10, choices = JOB_STATUS, default=JOB_STATUS[0][0])
  
  job_type = models.CharField(
      max_length=15, choices=JobType.choices, default=JobType.Full_Time
  )
  job_required_experience_type = models.CharField(
      max_length=30,
      choices=ExperienceType.choices,
      default=ExperienceType.Associate,
  )
  
  # Many-to-one Relationship
  company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_belong_to_company')
  
  # Many-to-many Relationship
  ##### A job can require many qualifications, a qualification can belong to many jobs
  job_required_qualifications = models.ManyToManyField(Qualification, related_name='job_required_qualifications')
  
  ##### A job can require many skills, a skill can be required many jobs
  job_required_skills = models.ManyToManyField(Skill, related_name='job_required_skills')

  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f'{self.title} from {self.company.company_name}'
  
class JobApplication(models.Model):
  STATUS = (
    ('Applied', 'Applied'),
    ('Screening', 'Screening'),
    ('Interview', 'Interview'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
  )
  candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='jobApplication_applied_by_candidate')
  job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='jobApplication_applying_under_job')
  status = models.CharField(max_length=255, null=True, choices=STATUS, default=STATUS[0][0])
  applied_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ('-updated_at', )
    
  def __str__(self):
    return f"{self.candidate} applying {self.job}"

class SkillSimilarities(models.Model):
  job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_skill_match')
  candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_skill_match')
  score = models.DecimalField(decimal_places=2, max_digits=5)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ('-score', )
    
  def __str__(self):
    return f'{self.score}'
    
class InterviewScoring(models.Model):
  application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='interview_score_application')
  overall_score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
  intellectual_curious_score = models.DecimalField(decimal_places=2, max_digits=5, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  self_motivation_score = models.DecimalField(decimal_places=2, max_digits=5, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  articulate_score = models.DecimalField(decimal_places=2, max_digits=5, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  analytical_and_product_minded_score = models.DecimalField(decimal_places=2, max_digits=5, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  remarks = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ('-overall_score', )
    
  def __str__(self):
    return f'{self.overall_score}'
  
class Scorecard(models.Model):
  application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='application_scorecard')
  overall_score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
  skill_score = models.ForeignKey(SkillSimilarities, on_delete=models.CASCADE, related_name='skill_score')
  qualification_score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
  social_media_score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
  interview_score = models.ForeignKey(InterviewScoring, on_delete=models.CASCADE, related_name='interview_score')
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ('-overall_score', )
    
  def __str__(self):
    return f"Scorecard for {self.application}"
  

  