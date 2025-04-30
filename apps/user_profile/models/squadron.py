from django.db import models
from django.conf import settings
from django.utils import timezone

class Squadron(models.Model):
    """Model representing a squadron."""
    
    # Fields
    name = models.CharField(
        max_length=100,
        help_text="Enter the squadron name"
    )
    url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Enter the squadron's website URL (optional)"
    )
    date_created = models.DateTimeField(
        auto_now_add=True, 
        null=True
    )
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True,
        related_name='squadrons'
    )

    # Methods
    
    def __str__(self):
        return self.name
        
    # Metadata

    class Meta:
        ordering = ["-name"]
        verbose_name_plural = "Squadrons" 