from django.db import models
from ..accounts.models import Candidate

class Qualification(models.Model):
  TYPE = (
    ('Certificate', 'Certificate'),
    ('Diploma', 'Diploma'),
    ('Bachelor', 'Bachelor'),
    ('Master', 'Master'),
    ('PhD', 'PhD'),
  )
  qualification_type = models.CharField(max_length=15, choices=TYPE, default='Bachelor')
  qualification_name = models.CharField(max_length=255, null=False)
  
  def get_qualification_type(self):
    return self.qualification_type
  
  def get_qualification_name(self):
    return self.qualification_name
  
  def __str__(self):
    return f'{self.qualification_type} in {self.qualification_name}'


# A candidate can have many candidate qualifications, a candidate qualification belongs to one candidate
class CandidateQualification(models.Model):
  candidate = models.ForeignKey(
    Candidate, null=True,
    on_delete=models.CASCADE, related_name='qualification_belongs_to_candidate'
  )
  qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE, related_name='candidate_qualification')
  
  institue_name = models.CharField(max_length=255, null=True)
  qualification_description = models.TextField()
  start_date = models.DateField(null=True)
  end_date = models.DateField(null=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)