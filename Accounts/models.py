from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Modify these fields to add related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # New related_name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # New related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )
    def __str__(self):
        return self.username
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)