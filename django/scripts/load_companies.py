from apps.accounts.models import Company
import csv

def run():
  with open('C:/Users/WT/OneDrive/Desktop/GitHub/projects/diversity-hire/extra/final_datasets/django/company.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      Company.objects.create(
        industry = row['industry'],
        company_name = row['name'],
        company_description = row['description'],
        address = row['address'],
        website_URL = row['url'],
        company_id = row['company_id']
      )