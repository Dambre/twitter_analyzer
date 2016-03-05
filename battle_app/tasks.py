from celery.decorators import periodic_task
from django.core import management


@periodic_task(run_every=(crontab(second='*/30'))name='update_hash_scores')
def update_hash(): 
    management.call_command('update_hash')
