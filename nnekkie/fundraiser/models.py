from django.db import models
from userauths.models import User
from .paystack import PayStack
import secrets
# Create your models here.



class Payment(models.Model):
    fund_date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    verified = models.BooleanField(default=False)
    email = models.EmailField()
    ref = models.CharField(max_length=500)

    class Meta:
        ordering = ['-fund_date']
    def __str__(self):
        return f'Payment : {self.amount}'
    
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            sim_ref = Payment.objects.filter(ref=ref)
            if not sim_ref:
                self.ref = ref
                
        super().save(*args,**kwargs)

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount']/100 == self.amount:
                self.verified = True
            self.save()

            if self.verified:
                return True
        return False
    def amount_value(self) -> int:
        return self.amount * 100
    