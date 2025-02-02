from django.db import models
from userauths.models import User
from django.utils import timezone
import pathlib
from django.utils.text import Truncator
from userauths.models import user_directory_path
from django.conf import settings
from django.utils.html import format_html
from facebook_prj.env import config
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import stripe
from facebook_prj.storages.backends import ProtectedStorage
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY
PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = ProtectedStorage()
# Create your models here.
class Product(models.Model):
    # strip product id
    image = models.ImageField(upload_to='product/',blank=False, null=False, default='cover.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    stripe_product_id = models.CharField(max_length=220, null=True, blank=True)
    name = models.CharField(max_length=120)
    description = models.TextField(default='')
    handle = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10,decimal_places=2, default=9.99)
    stripe_price = models.IntegerField(default=999)
    stripe_price_id = models.CharField(max_length=220, null=True, blank=True)
    price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def truncated_description(self):
        if self.description:  # Check if description is not None
            return Truncator(self.description).words(10)
        return ""  # Return an empty string if description is None

    # Remaining description after the truncation
    def remaining_description(self):
        if self.description:  # Check if description is not None
            truncated = Truncator(self.description).words(10)
            return self.description[len(truncated):].strip()
        return ""  # Return an empty string if description is None
    # Combine both descriptions with HTML formatting
    def formatted_description(self):
        truncated = self.truncated_description()
        remaining = self.remaining_description()
        return format_html(
            '<p>{}</p><p style="color: gray;">{}</p>',
            truncated,
            remaining if remaining else "No remaining content."
        )
    @property
    def display_price(self):
        return self.price
    
    def get_absolute_url(self, **kwargs):
        return reverse("product:detail", kwargs={'handle':self.handle})
    
    def get_manage_url(self, **kwargs):
        return reverse("product:manage", kwargs={'handle':self.handle})
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure a Stripe Product exists
        if not self.stripe_product_id:
            stripe_product = stripe.Product.create(name=self.name)
            self.stripe_product_id = stripe_product.id

        # Handle price changes and Stripe Price creation
        self.stripe_price = int(self.price * 100)  # Convert to cents
        if not self.stripe_price_id or self.price != self.og_price:
            stripe_price_obj = stripe.Price.create(
                product=self.stripe_product_id,
                unit_amount=self.stripe_price,
                currency="ngn",
            )
            self.stripe_price_id = stripe_price_obj.id
            self.price_changed_timestamp = timezone.now()

        # Save the original price if it changed
        if self.price != self.og_price:
            self.og_price = self.price

        super().save(*args, **kwargs)
def handlde_product_attachment_upload(instance, filename):
    return f"products/{instance.product.handle}/attachment/{filename}"
class ProductAttachment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    book = models.FileField(upload_to=handlde_product_attachment_upload,storage=protected_storage, null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=30, default="No data represented here")
    is_free = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product} : {self.book}"
    # def save(self, *args, **kwargs):
    #     if not self.name:
    #         self.name = pathlib.Path(self.book.name).name
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.name and self.book:  # Check if book is not None
            self.name = pathlib.Path(self.book.name).name
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return self.name or pathlib.Path(self.book.name).name
    
    def get_download_url(self, **kwargs):
        return reverse("product:download", kwargs={'handle':self.product.handle, 'pk':self.pk})