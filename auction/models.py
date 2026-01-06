from django.db import models
from django.conf import settings
from django.utils import timezone

class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/')
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    title: str = models.CharField(max_length=255)
    description: str = models.TextField()
    is_active: bool = models.BooleanField(default=True)

    def is_expired(self) -> bool:
        return timezone.now() > self.end_date

class Bid(models.Model):
    item = models.ForeignKey(Item, related_name='bids', on_delete=models.CASCADE)
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bids', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    item = models.ForeignKey(Item, related_name='questions', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_text = models.TextField()
    reply_text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply_timestamp = models.DateTimeField(null=True, blank=True)