from django.db import models
from django.utils import timezone
from .tag_utils import generate_tags
import logging

logger = logging.getLogger(__name__)

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
        return f"{self.title} ({self.status})"
    
    def save(self, *args, **kwargs):
        logger.debug(f"Starting save for item: {self.title}")
        is_new = self.pk is None
        logger.debug(f"Is new item: {is_new}")
        
        # First save the item to get an ID
        super().save(*args, **kwargs)
        logger.debug(f"Basic save completed. Item ID: {self.pk}")
        
        # Generate tags if none exist
        current_tags = self.tags.count()
        logger.debug(f"Current tag count: {current_tags}")
        
        if current_tags == 0:
            logger.debug("No existing tags found, generating new tags")
            try:
                generated_tags = generate_tags(self.title, self.description)
                logger.debug(f"Generated tags: {generated_tags}")
                
                # Create or get tags and add them to the item
                for tag_name in generated_tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    logger.debug(f"{'Created' if created else 'Found existing'} tag: {tag_name}")
                    self.tags.add(tag)
                
                logger.debug(f"Final tag count: {self.tags.count()}")
            except Exception as e:
                logger.error(f"Error generating tags: {str(e)}")
        else:
            logger.debug(f"Item already has {current_tags} tags")
