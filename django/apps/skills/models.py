from django.db import models
from ..accounts.models import Candidate

class Skill(models.Model):
  skill_name = models.CharField( max_length=255, null=False)
  
  def __str__(self):
    return self.skill_name

class CandidateSkill(models.Model):
  candidate = models.ForeignKey(
    Candidate,
    on_delete=models.CASCADE, related_name='skill_belongs_to_candidate'
  ) 
  skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='candidate_skill')