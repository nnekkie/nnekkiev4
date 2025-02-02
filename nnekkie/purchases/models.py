from django.db import models
from userauths.models import User
from django.utils import timezone
import pathlib
from userauths.models import user_directory_path
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))
from product.models import *
# Create your models here.
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    stripe_checkout_session_id = models.CharField(max_length=220, null=True, blank=True)
    completed = models.BooleanField(default=False)
    stripe_price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def display_price(self):
        return self.price
    def __str__(self):
        return f"{self.user} => {self.product} : {self.stripe_price}"

