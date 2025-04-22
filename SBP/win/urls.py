from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('competitions/create', CompetitionCreateView.as_view(), name='create-competition'),
    path('competitions/', CompetitionListView.as_view(), name='competition-list'),
    path('teams/', TeamCreateView.as_view(), name='create-team'),
    path('invitations/', InvitationCreateView.as_view(), name='create-invitation'),
    path('user/invitations/', UserInvitationsView.as_view(), name='user-invitations'),
    path('invitations/<int:pk>/respond/', InvitationResponseView.as_view(), name='invitation-respond'),
    path('team-applications/', TeamApplicationCreateView.as_view(), name='team-application-create'),
    path('team-applications/<int:pk>/response/', TeamApplicationResponseView.as_view(), name='team-application-response'),
    path('user-applications/', UserApplicationCreateView.as_view(), name='user-application-create'),
    path('faq/', FAQListView.as_view(), name='faq-list'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('roles/', RoleListView.as_view(), name='roles-list'),
    path('regions/', RegionListView.as_view(), name='regions-list'),
    path('disciplines/', DisciplineListView.as_view(), name='disciplines-list'),
    path('organizer/applications/', OrganizerApplicationsListView.as_view(), name='organizer-applications'),
    path('user-applications/<int:pk>/response/', ApplicationDecisionView.as_view(), name='user-application-decision'),
]
