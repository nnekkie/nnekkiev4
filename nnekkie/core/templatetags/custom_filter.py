from django import template
from django.utils import timezone
import datetime

register = template.Library()


@register.filter(name='count_filter')
def count_filter(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value  # Return the original value if it cannot be converted to an integer
    
    if value < 1000:
        return value  # No formatting for values less than 1000
    elif 1000 <= value < 1000000:
        return f"{value / 1000:.1f}k"  # Format thousands as "x.xk"
    elif value >= 1_000_000:
        return f"{value / 1000000:.1f}M"  # Format millions as "x.xM"



@register.filter(name='is_video')
def is_video(file):
    return file.lower().endswith(('.mp4', '.webm', '.mov', '.avi'))
  
@register.filter(name='is_image')
def is_video(file):
    return file.lower().endswith(('.png','.jpg','.jpeg','.gif'))
@register.filter(name='time_ago')
def time_ago(value):
    if not value:
        return ''
    
    now = timezone.now()
    diff = now - value
    
    if diff <= datetime.timedelta(minutes=1):
        return "just now"
    
    if diff <= datetime.timedelta(hours=1):
        minutes = diff.total_seconds() // 60
        return f"{int(minutes)} minutes ago"
    
    if diff <= datetime.timedelta(days=1):
        hours = diff.total_seconds() // 3600
        return f"{int(hours)} hours ago"
    
    if diff <= datetime.timedelta(weeks=1):
        days = diff.total_seconds() // 86400
        return f"{int(days)} days ago"
    
    if diff <= datetime.timedelta(weeks=4):
        weeks = diff.total_seconds() // (86400 * 7)
        return f"A week ago" if weeks == 1 else f"{int(weeks)} weeks ago"
    
    months = diff.total_seconds() // (86400 * 30)
    return f"{int(months)} month ago" if months == 1 else f"{int(months)} months ago"
