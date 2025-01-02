from django.db import models

class Item(models.Model):
    LOST = 'lost'
    FOUND = 'found'
    ITEM_TYPE_CHOICES = [
        (LOST, 'Lost'),
        (FOUND, 'Found'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    contact_info = models.CharField(max_length=200)
    item_type = models.CharField(max_length=5, choices=ITEM_TYPE_CHOICES)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_item_type_display()} item: {self.name}"

    class Meta:
        ordering = ['-date']
