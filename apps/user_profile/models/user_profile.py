from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz

class UserProfile(models.Model):
    """Model representing a user profile with additional information."""
    
    # One-to-One relationship with the User model
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Profile image using ResizedImageField for automatic resizing
    avatar = ResizedImageField(
        verbose_name="Profile Picture",
        size=[200, 200],
        crop=['middle', 'center'],
        upload_to="profiles/avatars/",
        help_text="User profile picture",
        null=True,
        blank=True,
    )
    
    # Timezone field with choices from pytz
    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]
    
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default='UTC',
        help_text="User's preferred timezone"
    )
    
    # Foreign key to Squadron model
    squadron = models.ForeignKey(
        'Squadron',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        help_text="The squadron this user belongs to"
    )
    
    # Additional fields
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Short biography"
    )
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# Signal to create a UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile for a new User."""
    if created:
        UserProfile.objects.create(user=instance)

# Signal to save the UserProfile when the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved."""
    instance.profile.save() 