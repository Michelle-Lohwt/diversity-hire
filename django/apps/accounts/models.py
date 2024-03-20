from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group
)

ADMIN = 'Admin'
COMPANY = 'Company'
RECRUITER = 'Recruiter'
CANDIDATE = 'Candidate'

ROLES = [(ADMIN, 'Admin'), (COMPANY, 'Company'), (RECRUITER, 'Recruiter'), (CANDIDATE, 'Candidate')]
GENDER = (("Male", "Male"), ("Female", "Female"))

# Account
class BaseAccountManager(BaseUserManager):
  def _create_user(self, username, password, **extra_fields):
    """
    Creates and saves a User with the given username and password.
    """
    if not username:
        raise ValueError("Users must have an username")

    username = username.lower()

    user = self.model(username=username, **extra_fields)

    user.set_password(password)
    user.save(using=self._db)
    
    role = extra_fields.get('role')
    group = Group.objects.get(name=role)
    group.user_set.add(user)
    
    return user

  def create_user(self, username, password, **extra_fields):
    try:
      Group.objects.get(name='Recruiter')
    except:
      Group.objects.create(name='Recruiter')
    
    try:
      Group.objects.get(name='Candidate')
    except:
      Group.objects.create(name='Candidate')
      
    extra_fields.setdefault("is_staff", False)      # Indicates whether a user is considered staff and has access to the Django admin
    extra_fields.setdefault("is_superuser", False)  # Indicates whether a user is a superuser with full access to the system and all functionalities.
    extra_fields.setdefault("is_active", True)      # Indicates whether a user is enabled and can log in to the system
    return self._create_user(username, password, **extra_fields)

  def create_superuser(self, username, password, **extra_fields):
    try:
      Group.objects.get(name='Admin')
    except Group.DoesNotExist:
      Group.objects.create(name='Admin')
    
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)
    return self._create_user(username, password, **extra_fields)


# Create a base account model that inherits from AbstractBaseUser
class BaseAccount(AbstractBaseUser, PermissionsMixin):
  # Define the username as the unique identifier for users
  username = models.CharField(
    verbose_name="username",
    max_length=150,
    unique=True,
  )

  # Define role, date joined, and last modified
  name = models.CharField(verbose_name="name", max_length=300, blank=True)
  role = models.CharField(max_length=50, choices=ROLES, default = CANDIDATE)
  
  date_joined = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  
  objects = BaseAccountManager()

  # Specify the USERNAME_FIELD attribute
  USERNAME_FIELD = "username"
  REQUIRED_FIELDS = ["name", "role"]
  
  def get_role(self):
    return self.role
  
  def __str__(self):
    return self.name



# Candidate
class Candidate(models.Model):
  user = models.OneToOneField(
    BaseAccount,
    on_delete=models.CASCADE, related_name='candidate_profile'
  )  # one profile for one account (that's unique)

  # Define fields for first name, last name, gender, phone number, and date of birth
  gender = models.CharField(verbose_name="gender", max_length=10, choices=GENDER)
  phone_number = models.CharField(verbose_name="phone number", max_length=255, null=True)
  date_of_birth = models.DateField(verbose_name="date of birth", null=True)

  candidate_summary = models.TextField(null=True)
  linkedIn_URL = models.URLField(null=True)
  insta_URL = models.URLField(null=True)
  other_social_media_URL = models.URLField(null=True)
  
  def __str__(self):
    return self.user.name

class Experience(models.Model):
  candidate = models.ForeignKey(
    Candidate, null=True,
    on_delete=models.CASCADE, related_name='experience_belongs_to_candidate'
  )
  job_title = models.CharField(max_length=255)
  job_description = models.TextField()
  company_name = models.CharField(max_length=255, null=False)
  is_current_job = models.BooleanField(default=False)
  start_date = models.DateField(null=False)
  end_date = models.DateField(null=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)



# Recruiter
class Recruiter(models.Model):
  user = models.OneToOneField(
    BaseAccount,
    on_delete=models.CASCADE, related_name='recruiter_profile'
  )  # one profile for one account (that's unique)
  
  gender = models.CharField(
    verbose_name="gender", max_length=10, choices=GENDER, null=False
  )
  contact_number = models.CharField(
    verbose_name="contact number", max_length=255, null=True
  )
  date_of_birth = models.DateField(verbose_name="date of birth", null=True)

  recruiter_title = models.CharField(max_length=255, null=False,)
  recruiter_summary = models.TextField(null=True)
  linkedIn_URL = models.URLField(null=True)
  
  def __str__(self):
    return self.user.name


# Company
class Industry(models.TextChoices):
  Business_Management = "Business and Management"
  IT = "Information Technology"
  Human_Resource = "Human Resource"
  Healthcare = "Healthcare"
  Banking_Finance = "Banking and Finance"
  Engineering_Manufacturing = "Engineering and Manufacturing"
  Education = 'Education'

class Company(models.Model):
  industry = models.CharField(
      max_length=30, choices=Industry.choices, default=Industry.Business_Management
  )
  
  company_name = models.CharField(verbose_name="company name", max_length=255, null=False)
  company_description = models.TextField(null = True)
  address = models.TextField(null=True)
  website_URL = models.URLField()
  company_id = models.FloatField(null=True)
  
  class Meta:
    verbose_name_plural = 'companies'
    
  def __str__(self):
    return self.company_name