from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('blog/<slug:slug>/', blog_detail, name='blog-detail', ),
    path('blog-dashboard/',blog_home ,name='blog-dashboard'),
    path('blog-dashbord/<username>/',blogger_profile, name='dashboard'),
    path('follow-blogger/', follow_blogger, name='follow'),
    # Ajax url 
    path('like-blog/', like_blog, name='like-blog'),
    path('comment-blog/', comment_on_blog, name='comment-on-blog'),
    path('like-blog-comment/', like_blog_comment, name='like-blog-comment'),
    path('reply-blog-comment/', reply_blog_comment, name='reply-blog-comment'),
    path('delete-blog-comment/', delete_blog_comment, name='delete-blog-comment'),
    path('create-blog/', create_blog, name='create-blog'),
    path('delete-blog/', delete_blog, name='delete-blog'),
]