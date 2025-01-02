from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    ITEM_STATUS = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=5, choices=ITEM_STATUS)
    contact_info = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return f"{self.get_status_display()}: {self.title}"
