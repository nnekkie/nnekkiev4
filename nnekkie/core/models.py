from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.dispatch import receiver

from userauths.models import User, Profile, user_directory_path

from PIL import Image
from shortuuid.django_fields import ShortUUIDField
import shortuuid
import os

import random
from django.urls import reverse

VISIBILITY = (
    ("Only Me","Only Me"),
    ("Everyone","Everyone"),
)

FRIEND_REQUEST = (
    ("pending","pending"),
    ("accept","Accept"),
    ("reject","Reject"),
)


NOTIFICATION_TYPE = (
    ("Friend Request", "Friend Request"),
    ("Friend Request Accepted", "Friend Request Accepted"),
    ("New Follower", "New Follower"),
    ("New Like", "New Like"),
    ("New Comment", "New Comment"),
    ("Comment Liked", "Comment Liked"),
    ("Comment Replied", "Comment Replied"),
    

)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, blank=True ,null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default="everyone", choices=VISIBILITY)
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'untitled'
    
    def get_absolute_url(self):
        return reverse('core:feed')
    
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Post"
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + "-" + str(uniqueid.lower())
        super(Post, self).save(*args, **kwargs) 

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))
    
    def gallery_images(self):
        return Gallery.objects.filter(post=self)
    
    def title_len_count(self):
        return len(self.title)
    
    def galley_img_count(self):
        return Gallery.objects.filter(post=self).count()

    def post_comments(self):
        comments = Comment.objects.filter(post=self, active=True)
        return comments
    
    def post_comments_count(self):
        comments_count = Comment.objects.filter(post=self, active=True).count()
        return comments_count
    

@receiver(models.signals.pre_delete, sender=Post)
def delete_image_file(sender, instance, **kwargs):
    # Check if the image field has a value
    if instance.image:
        # Get the path of the image file
        image_path = instance.image.path
        # Check if the image file exists
        if os.path.exists(image_path):
            # Delete the image file
            os.remove(image_path)


class Gallery(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="gallery", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.post)
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Gallery"

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 30px;" />' % (self.image))


class FriendRequest(models.Model):
    fid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="request_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="request_receiver")
    status = models.CharField(max_length=10, default="pending", choices=FRIEND_REQUEST)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}"
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Friend Request"

class Friend(models.Model):
    fid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Friend"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True ,null=True)
    date = models.DateTimeField(auto_now_add=True)
    cid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likes")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Comment"

    def comment_replies(self):
        comment_replies = ReplyComment.objects.filter(comment=self, active=True)
        return comment_replies


class ReplyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.CharField(max_length=500, blank=True ,null=True)
    date = models.DateTimeField(auto_now_add=True)
    cid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Reply Comment"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="noti_user")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="noti_sender")
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name="noti_post")
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True, related_name="noti_comment")
    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, default="none")
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    nid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"


class Group(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    memebers = models.ManyToManyField(User, blank=True, related_name="memebers")
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True, default='cover.jpg')
    name = models.CharField(max_length=500, blank=True ,null=True)
    description = models.TextField(blank=True ,null=True)
    gid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Group"
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
        super(Group, self).save(*args, **kwargs) 

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))
    
    def memeber_count(self):
        return self.memebers.all().count()
    

class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500, blank=True ,null=True)
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default="everyone", choices=VISIBILITY)
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    likes = models.ManyToManyField(User, blank=True, related_name="group_post_likes")
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Group Post"
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
    
    # Fallback to 'untitled' if no title
        if not self.title:
            self.title = "untitled"
    
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(uniqueid.lower())
    
        super(GroupPost, self).save(*args, **kwargs)
    def group_post_comment(self):
        comment  = list(GroupPostComment.objects.filter(post=self, active=True))
        random.shuffle(comment)
        return comment
    

    def thumbnail(self):
        if not self.file:
            return "No file"

        ext = os.path.splitext(self.file.name)[1].lower()
    
    # Check if file is an image
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return mark_safe(
                f'<img src="{self.file.url}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />'
            )
    
    # Check if file is a video
        elif ext in ['.mp4', '.mov', '.avi', '.webm']:
            return mark_safe(
                f'''
                <video width="60" height="60" style="border-radius: 5px;" muted>
                    <source src="{self.file.url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                '''
            )
    
    # Return placeholder for unsupported files
        return mark_safe('<span style="color: gray;">Unsupported file type</span>')


class GroupPostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True ,null=True)
    date = models.DateTimeField(auto_now_add=True)
    cid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    likes = models.ManyToManyField(User, blank=True, related_name="group_comment_likes")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Group Post Comment"

    def comment_replies(self):
        comment_replies = GroupPostReplyComment.objects.filter(comment=self, active=True)
        return comment_replies

class GroupPostReplyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(GroupPostComment, on_delete=models.CASCADE)
    reply = models.CharField(max_length=500, blank=True ,null=True)
    date = models.DateTimeField(auto_now_add=True)
    cid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Reply Group Post Comment"


class Snaps(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default="everyone", choices=VISIBILITY)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    gid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")

    def desc(self):
        return self.description[:20]

    def __str__(self):
        return f'{self.user.username} : posted'
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Snaps"
    
    # def save(self, *args, **kwargs):
    #     uuid_key = shortuuid.uuid()
    #     uniqueid = uuid_key[:4]
    #     if self.slug == "" or self.slug == None:
    #         self.slug = slugify(self.gid) + "-" + str(uniqueid.lower())
    #     super(Snaps, self).save(*args, **kwargs) 

    def thumbnail(self):
        if self.video:
            return mark_safe("<video width='50' height='50' controls><source src='/media/%s' type='video/mp4'></video>"%(self.video))
    def followers_count(self):
        return self.followers.all().count()

class SnapViews(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    snap = models.ForeignKey(Snaps, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['users','snap']
        
class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name="page_followers")
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    name = models.CharField(max_length=500, blank=True ,null=True)
    description = models.TextField(blank=True ,null=True)
    visibility = models.CharField(max_length=10, default="everyone", choices=VISIBILITY)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    gid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")

    def desc(self):
        return self.description[:20]

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Page"
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
        super(Page, self).save(*args, **kwargs) 

    def thumbnail(self):
        if self.image:
            return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))
        if self.video:
            return mark_safe("<video width='50' height='50' controls><source src='/media/%s' type='video/mp4'></video>"%(self.video))
    def followers_count(self):
        count =  self.followers.all().count()
        if count >= 1000000:
            return f"{count/1000000:.1f}M"
        if count >= 1000:
            return f"{count/1000:.1f}K"
        if count == 0:
            return "None"
        else :
            formatted_count = str(count)

        return formatted_count

class PagePost(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    file  = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    title = models.TextField()

    def __str__(self):
        if self.title:
            return self.title
        else :
            return 'untitled post'


    

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="chat_user")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    mid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Personal Chat"

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))
    
    
    
class GroupChat(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    images = models.FileField(upload_to="group_chat", blank=True, null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="group_host")
    members = models.ManyToManyField(User, related_name="group_chat_members")
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Group Chat"
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
        super(GroupChat, self).save(*args, **kwargs) 

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))
    
    def last_message(self):
        last_message = GroupChatMessage.objects.filter(groupchat=self).order_by("-id").first()
        return last_message

class GroupChatMessage(models.Model):
    groupchat = models.ForeignKey(GroupChat, on_delete=models.SET_NULL, null=True, related_name="group_chat")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="group_chat_message_sender")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    mid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    
    
    def __str__(self):
        return self.groupchat.name
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Group Chat Messages"
