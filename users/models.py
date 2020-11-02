from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    last_location = models.PointField(
        editable=False,
        blank=True,
        null=True,
        default=None)

    # Returns the string representation of the model.
    def __str__(self):
        return f"{self.user}"


@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    try:
        my_profile = instance.profile
        my_profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
