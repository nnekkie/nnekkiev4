from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import *


@shared_task
def delete_old_task():
    day_ago = timezone.now() - timedelta(days=1)
    old_snaps = Snaps.objects.filter(date__lte=day_ago, active=True)
    deleted_count = old_snaps.delete()[0]
    
