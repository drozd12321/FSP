from django.urls import path
from .views import *

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='users-list'),
    path('user-profile/', UserProfileView.as_view(), name='profile-actions'),
    path('approvals/', UserApprovalView.as_view(), name='user-approvals'),
    
    path('competitions/create/', CompetitionCreateView.as_view(), name='create-competition'),
    path('competitions/', CompetitionListView.as_view(), name='competition-list'),
    path('competitions/history/', ParticipationHistoryView.as_view(), name='participation-history'),
    path('competitions/organized/', OrganizedCompetitionsView.as_view(), name='organized-competitions'),
    path('competitions/pending/', PendingCompetitionsView.as_view(), name='pending-competitions'),
    path('competitions/decision/', CompetitionDecisionView.as_view(), name='competition-decision'),
    path('competitions/distribute-results/', DistributeResultsView.as_view(), name='distribute-results'),
    path('competitions/<int:competition_id>/participants/', CompetitionParticipantsView.as_view(), name='competition-participants'),
    path('competitions/status/', CompetitionStatusView.as_view(), name='competition-status'),
    
    path('teams/', TeamCreateView.as_view(), name='create-team'),
    path('teams/public/', PublicTeamsView.as_view(), name='public-teams'),
    path('user/teams/', UserTeamsView.as_view(), name='user-teams'),
    path('vacancy-responses/', CaptainVacancyResponsesView.as_view(), name='captain-vacancy-responses'),
    path('response-to-public/', ResponseToPublicView.as_view(), name='response-to-public'),
    path('response-action/', ResponseActionView.as_view(), name='response-action'),
    
    path('invitations/', InvitationCreateView.as_view(), name='create-invitation'),
    path('user/invitations/', UserInvitationsView.as_view(), name='user-invitations'),
    path('invitations/<int:pk>/respond/', InvitationResponseView.as_view(), name='invitation-respond'),
    path('team-applications/', TeamApplicationCreateView.as_view(), name='team-application-create'),
    path('team-applications/<int:pk>/response/', TeamApplicationResponseView.as_view(), name='team-application-response'),
    path('user-applications/', UserApplicationCreateView.as_view(), name='user-application-create'),
    path('user-applications/<int:pk>/response/', ApplicationDecisionView.as_view(), name='user-application-decision'),
    path('organizer/user/applications/', OrganizerUserApplicationsListView.as_view(), name='organizer-user-applications'),
    path('organizer/team/applications/', OrganizerTeamApplicationsListView.as_view(), name='organizer-team-applications'),
    
    path('faq/', FAQListView.as_view(), name='faq-list'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('roles/', RoleListView.as_view(), name='roles-list'),
    path('regions/', RegionListView.as_view(), name='regions-list'),
    path('disciplines/', DisciplineListView.as_view(), name='disciplines-list'),
    path('regional-representatives/', RegionalRepresentativesView.as_view(), name='regional-representatives'),
]
