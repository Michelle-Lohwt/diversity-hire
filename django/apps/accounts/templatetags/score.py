from django.template import Library

register = Library()

@register.filter
def score(applications, candidate):
  score = (applications.get(candidate = candidate)).score
  return score