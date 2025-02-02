from django.db import models
from userauths.models import User, user_directory_path
import shortuuid
from django.urls import reverse
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe, format_html
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
# Create your models here.



class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  default=None)
    title = models.TextField()
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    likes = models.ManyToManyField(User, blank=True, related_name='blog_likes')
    views = models.PositiveIntegerField(default=0)
    bid = ShortUUIDField(length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvwxyz')
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        current_site = Site.objects.get_current()
        domain = current_site.domain
        return f'http://{domain}{reverse("blog:blog-detail", args=[str(self.pk)])}'

    def caption(self):
        return self.title[:20]
    
    caption.short_description = 'Title'
    def __str__(self):
        return self.title
    class Meta:

        ordering = ['date']
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        unique_id = uuid_key[:2]
        if self.slug == '' or self.slug== None:
            self.slug = slugify(self.title)+'-'+str(unique_id.lower())

        super(Blog, self).save(*args, **kwargs)

    def thumbnail(self):
        if self.file:
            if self.file.url.lower().endswith(('.png','.jpg','.jpeg','.gif')):
                return mark_safe("<img src='%s' width='40' height='40' style='object-fit:cover;' />" % self.file.url)
            if self.file.url.lower().endswith(('.mp4','.webm','.ogg')):
                return mark_safe("<video width='50' height='50' controls><source src='%s' type='video/mp4'></video>" % self.file.url)
            return 'no tag'
        
    def like_count(self):
        count = self.likes.count()

        return count
    like_count.short_description = 'Likes'

    def blog_comment(self):
        comment = Comment.objects.filter(blog=self, active=True).order_by('-date')
        return comment
    def blog_comment_count(self):
        comment_count = Comment.objects.filter(blog=self,active=True).count()
        return comment_count


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_user')
    comment = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='blog_comment_likes')
    cid  = ShortUUIDField(length=7, max_length=24, alphabet='abcdefghijklmnopqrstuvwxyz')

    def comment_replies(self):
        replies = ReplyComment.objects.filter(active=True, comment=self)
        return replies

    def __str__(self):
        return self.comment

    def comment_like_count(self):
        return self.likes.count()
    comment_like_count.short_description = 'likes'


class ReplyComment(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comment_reply_user')
    comment  = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.CharField(max_length=250, blank=True, null=True)
    date  = models.DateTimeField(auto_now_add=True)
    cid = ShortUUIDField(length=7, max_length=25, alphabet='abcdefghijklmnopqstuvwxyz')
    active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.user.username}: {self.reply}"
    class Meta:
        verbose_name_plural = 'Replies'
        

class FollowerRequest(models.Model):
    fid  = ShortUUIDField(max_length=25, length=7, alphabet='abcdefghijklmnopqrstuvwxyz')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_receiver')
    status = models.CharField(max_length=14, choices={'Accept':_('Accept'), 'Pending':_('Pending'), 'Reject':_('Reject')}, default='Pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} : {self.status}'