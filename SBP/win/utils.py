import math
from django.db.models import Count

def calculate_user_rating(user_info):
    """
    Формула: Σ[(N - position + 1) * log2(N + 1)] / sqrt(total_participations + 3) * 100
    Где:
    - N = количество участников в соревновании
    - position = занятое место
    """
    participations = user_info.competition_participations.select_related(
        'competition'
    ).annotate(
        total_participants=Count('competition__participants')
    )
    
    if not participations.exists():
        return 0.0
    
    total_score = 0.0
    total_participations = participations.count()
    
    for p in participations:
        n = p.total_participants
        position = p.result
        
        if n > 0 and position > 0:
            place_score = (n - position + 1) / n
            size_factor = math.log2(n + 1)
            total_score += place_score * size_factor
    
    normalized_rating = (total_score / math.sqrt(total_participations + 3)) * 100
    return round(normalized_rating, 2)