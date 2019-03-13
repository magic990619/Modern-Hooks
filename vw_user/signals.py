from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from vw_question.models import SampleQuestion, Position
from vw_user.default_templates import default_questions, default_invite_messages
from vw_user.models import InviteTemplate


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_templates(sender, instance, created, **kwargs):
    if created:
        position = Position.objects.create(user=instance, name='General')
        for q in default_questions:
            SampleQuestion.objects.create(
                user=instance, type='formal', content=q, position=position
            )
        for m in default_invite_messages:
            InviteTemplate(user=instance, html=m)
