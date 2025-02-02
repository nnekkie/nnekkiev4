from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from core.templatetags.custom_filter import *  # Adjust the import path as necessary
from  django.utils.text import slugify
from userauths.models import Profile, User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.
import random
import shortuuid

@csrf_exempt# Remove if you have CSRF middleware enabled properly in your project
def delete_blog(request):
    id =request.POST['id']
    post = Blog.objects.get(id=id, user=request.user)
    post.delete()
    data = {
        'bool':True
    }
    return JsonResponse({'data':data})
@login_required
def follow_blogger(request):
    blogger_id = request.GET.get('id')
    if request.user.is_anonymous:
        return JsonResponse({'error':"You must be logged in to follow this blogger"})
    to_follow = get_object_or_404(Profile, id=blogger_id)
    if request.user in to_follow.followers.all():
        to_follow.followers.remove(request.user)
        is_following = False
    else :
        to_follow.followers.add(request.user)
        is_following = True
        
    data = {
        'is_following':is_following,
        'followers':count_filter(to_follow.followers.count)
    }
    return JsonResponse({'data':data})

def blog_home(request):
    user = request.user
    blog= Blog.objects.filter(user=user, active=True)
    profile = Profile.objects.filter(user=user)

    context = {
        'blogs':blog,
        'profile':profile
    }
    return render(request, 'blog/my-blogs.html', context)

def blogger_profile(request, username):
    
    profile = Profile.objects.get(user__username=username)
    blog = Blog.objects.filter(user=profile.user, active=True)
    bool = False
    bool_follower = False
    sender = request.user
    receiver = profile.user
    try:
        follower_request = FollowerRequest.objects.get(sender=sender, receiver=receiver)
        if follower_request:
            bool = True
        else :
            bool =False

    except:
        bool =False

    context = {
        'profile':profile,
        'blogs': blog,
        'bool':bool,
        
    }

    return render(request, 'blog/blogger-profile.html', context)


@csrf_exempt
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('blog-title')
        file = request.FILES.get('blog-file')  # Use request.FILES for file uploads
        print('title ======', title)
        print('file =======', file)

        # Validate required fields
        if not title or not file:
            return JsonResponse({'error': 'Title and file are required'}, status=400)

        try:
            unique_id = shortuuid.uuid()
            blog = Blog.objects.create(
                title=title,
                file=file,
                user=request.user,
                slug=slugify(title) + '-' + str(unique_id.lower())
            )

            

            return JsonResponse({'blog': {
                'title': blog.title,
                'file': blog.file.url,
                'full_name':blog.user.username,
                'profile_image': blog.user.profile.image.url,
                'id': blog.id,
                'date': time_ago(blog.date)  # Ensure time_ago function is defined
            }})

        except Exception as e:
            print(f"Error creating blog: {e}")
            return JsonResponse({'error': 'An error occurred while creating the blog'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug, active=True)
    context = {'b':blog}
    return render(request, 'blog/blog-detail.html', context)


def delete_blog_comment(request):
    id = request.GET.get('id')
    comment = Comment.objects.get(id=id)
    comment.delete()

    data = {
        'bool':True
    }
    return JsonResponse({"data":data})

def reply_blog_comment(request):
    id = request.GET.get('id')
    reply = request.GET.get('reply')
    comment = Comment.objects.get(id=id)
    user  = request.user
    new_reply  = ReplyComment.objects.create(
        comment=comment,
        user=user,
        reply=reply
    )
    reply_count = ReplyComment.objects.filter(comment=comment).count()
    data  = {
        'reply':new_reply.reply,
        'profile_image': new_reply.user.profile.image.url,
        'date':time_ago(new_reply.date),
        'comment_id':new_reply.comment.id,
        'reply_id':new_reply.id,
        'replies':reply_count+ int(1)
    }
    return JsonResponse({'data':data})

def comment_on_blog(request):
    id = request.GET.get('id')
    comment = request.GET.get('comment')
    blog = Blog.objects.get(id=id)
    comment_count = Comment.objects.filter(blog=blog).count()
    user = request.user

    new_comment = Comment(
        blog=blog,
        comment=comment,
        user=user
    )
    new_comment.save()
    total_comments = Comment.objects.filter(blog=blog).count()
    remaining_comment = max(0, total_comments -2)
    data = {
        'bool':True,
        'comment':new_comment.comment,
        'profile_image': new_comment.user.profile.image.url,
        'username': new_comment.user.username,
        'fullname': new_comment.user.profile.full_name,
        'comment_id':new_comment.id,
        'blog_id':new_comment.blog.id,
        'date': time_ago(new_comment.date),
        'comment_count': comment_count + int(1),
        'remaining_comments':remaining_comment
    }
    return JsonResponse({"data":data})


def like_blog_comment(request):
    id = request.GET.get('id')
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False

    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False

    else :
        comment.likes.add(user)
        bool = True

    data = {
        'bool':bool,
        'likes':comment.likes.all().count()
    }

    return JsonResponse({'data':data})

def index(request):
    blog = Blog.objects.filter(active=True)
    context = {
        'blogs':blog
    }
    return render(request, 'blog/index.html', context)

#for liking of blog feature
def like_blog(request):
    id = request.GET.get('id')
    blog = Blog.objects.get(id=id)
    user = request.user
    bool = False

    if user in blog.likes.all():
        blog.likes.remove(user)
        bool = False
    else :
        blog.likes.add(user)
        bool = True

    data = {
        'bool':bool,
        'likes':blog.likes.all().count()
    }
    return JsonResponse({'data':data})