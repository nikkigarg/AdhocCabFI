from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


from accounts.models import Profile
from accounts.tasks import send_activation_mail


@receiver(signal=post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, created, **kwargs):
    # print(sender, instance, created, raw, using, update_fields)
    if created:
        Profile(user=instance).save()
    send_activation_mail.delay(instance)
