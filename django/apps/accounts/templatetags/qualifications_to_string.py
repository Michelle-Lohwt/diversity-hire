from django.template import Library
from collections import defaultdict

register = Library()

@register.filter
def qualifications_to_string(qualifications):
  """Concatenates qualifications with commas and removes trailing comma."""
  q_dict = defaultdict(list)
  for q in qualifications.values():
    q_dict[q['qualification_name']].append(q['qualification_type'])
    
  q_list = []
  for name, types in q_dict.items():
    concatenated_types = '/ '.join(types)  # Join types with comma and space
    q_list.append(concatenated_types + ' in ' + name)
    
  return q_list