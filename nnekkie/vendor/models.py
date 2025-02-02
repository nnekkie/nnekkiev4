from django.db import models
from userauths.models import User
# Create your models here.



class Vendor(models.Model):
    name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)


    class Meta:
        ordering = ['name', 'created_at']

    def __str__(self):
        return se;lf.name