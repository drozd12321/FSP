from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CompetitionParticipant

@receiver([post_save, post_delete], sender=CompetitionParticipant)
def update_user_rating(sender, instance, **kwargs):
    """Обновляем рейтинг при изменении участия"""
    instance.participant.update_rating()