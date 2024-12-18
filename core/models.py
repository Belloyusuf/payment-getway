from django.db import models
import secrets
from .paystack import Paystack

class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    verified = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)


    class Meta:
        ordering = ("-date_created", )


    def __str__(self) -> str:
        return f"Payment: {self.amount}"
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)

            if not object_with_similar_ref.exists():
                self.ref=ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100
    

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()

        if self.verified:
            return True
        return False
