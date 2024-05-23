from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .views import update_sentiment_score

def start():
  scheduler = BackgroundScheduler()
  scheduler.add_job(update_sentiment_score, 'interval', seconds=604800)
  scheduler.start()