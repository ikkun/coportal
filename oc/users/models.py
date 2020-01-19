from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


TEAM_CHOICES = (
    ("OPT1", "CO - OPT1"),
    ("OPT2", "CO - OPT2"),
    ("OPH", "CO - OPH"),
    ("SO", "CO - SO"),
    ("SA", "PS - SA"),
    ("OS", "PS - OS"),
    ("NM", "NO - NM"),    
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.CharField(max_length=100, choices=TEAM_CHOICES)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
