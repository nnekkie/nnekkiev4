from django.shortcuts import render
from core.models import Page, Friend
from django.db.models import Count
# Create your views here.


def page_index(request):
    user=request.user
    page = Page.objects.filter(active=True, visibility="Everyone")
    friend = Friend.objects.filter(user=user)
    page_followed_by_friend = Page.objects.filter(followers__in=[friend.friend for friend in friend])
    page_rank = page.annotate(num_followers=Count('followers')).order_by('-num_followers')
    context = {
        'page':page,
        'page_friend':page_followed_by_friend,
        'page_rank':page_rank
    }
    return render(request, 'addons/pages.html', context)
