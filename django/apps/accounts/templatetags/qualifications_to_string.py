from django.template import Library

register = Library()

@register.filter
def qualifications_to_string(qualifications):
  """Concatenates qualifications with commas and removes trailing comma."""
  q_type = qualifications.values('qualification_type').distinct()
  q_name = qualifications.values('qualification_name').distinct()
  
  q_list = []
  for q in q_name:
    q_list.append(q_type[0]['qualification_type'] + '/ ' + q_type[1]['qualification_type'] + ' in ' + q['qualification_name'])
  
  return q_list