from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('competitions/', CompetitionCreateView.as_view(), name='create-competition'),
    path('teams/', TeamCreateView.as_view(), name='create-team'),
    path('invitations/', InvitationCreateView.as_view(), name='create-invitation'),
    path('user/invitations/', UserInvitationsView.as_view(), name='user-invitations'),
    path('invitations/<int:pk>/respond/', InvitationResponseView.as_view(), name='invitation-respond'),
]
