from django.db import models
from userauths.models import User, Profile
from shortuuid.django_fields import ShortUUIDField
import shortuuid
# Create your models here.
class GroupChat(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    images = models.FileField(upload_to="group_chat", blank=True, null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="group_owner")
    members = models.ManyToManyField(User, related_name="group_members")
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
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="group_chat_message_sender_1")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    mid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    
    
    def __str__(self):
        return self.groupchat.name
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Group Chat Messages"