from django.urls import path
from .views import *

urlpatterns = [
    # Аутентификация
    path('api/auth/register/', RegisterView.as_view(), name='register'),  # Регистрация нового пользователя
    path('api/auth/login/', LoginView.as_view(), name='login'),  # Вход в систему
    
    # Пользователи
    path('users/', UserListView.as_view(), name='users-list'),  # Список всех пользователей
    path('user-profile/', UserProfileView.as_view(), name='profile-actions'),  # Профиль пользователя (CRUD)
    path('approvals/', UserApprovalView.as_view(), name='user-approvals'),  # Одобрение/отклонение регистрации пользователей
    
    # Соревнования
    path('competitions/download/', CompetitionParticipantsStructuredExportAPI.as_view()), # Выгрузка соревнований и их результатов в файл
    path('competitions/create/', CompetitionCreateView.as_view(), name='create-competition'),  # Создание соревнования
    path('competitions/', CompetitionListView.as_view(), name='competition-list'),  # Список всех соревнований
    path('competitions/history/', ParticipationHistoryView.as_view(), name='participation-history'),  # История участий в соревнованиях
    path('competitions/organized/', OrganizedCompetitionsView.as_view(), name='organized-competitions'),  # Соревнования, организованные пользователем
    path('competitions/pending/', PendingCompetitionsView.as_view(), name='pending-competitions'),  # Соревнования на модерации
    path('competitions/decision/', CompetitionDecisionView.as_view(), name='competition-decision'),  # Решение по соревнованию (одобрить/отклонить)
    path('competitions/distribute-results/', DistributeResultsView.as_view(), name='distribute-results'),  # Распределение результатов соревнования
    path('competitions/<int:competition_id>/participants/', CompetitionParticipantsView.as_view(), name='competition-participants'),  # Участники конкретного соревнования
    path('competitions/status/', CompetitionStatusView.as_view(), name='competition-status'),  # Обнолвение статусов соревнований
    path('competitions/region/<int:region_id>/', RegionCompetitionsView.as_view(), name='region-competitions'),  # Соревнования по региону
    
    # Команды
    path('teams/', TeamCreateView.as_view(), name='create-team'),  # Создание команды
    path('teams/public/', PublicTeamsView.as_view(), name='public-teams'),  # Публичные команды
    path('user/teams/', UserTeamsView.as_view(), name='user-teams'),  # Команды пользователя
    
    # Отклики на вакансии
    path('vacancy-responses/', CaptainVacancyResponsesView.as_view(), name='captain-vacancy-responses'),  # Отклики для капитана
    path('response-to-public/', ResponseToPublicView.as_view(), name='response-to-public'),  # Отправка отклика на публичную вакансию
    path('response-action/', ResponseActionView.as_view(), name='response-action'),  # Действия с откликом (принять/отклонить)
    path('user/vacancy-responses/', UserVacancyResponsesView.as_view(), name='user-vacancy-responses'),  # Отклики пользователя
    
    # Приглашения и заявки
    path('invitations/', InvitationCreateView.as_view(), name='create-invitation'),  # Создание приглашения
    path('user/invitations/', UserInvitationsView.as_view(), name='user-invitations'),  # Приглашения пользователя
    path('invitations/<int:pk>/respond/', InvitationResponseView.as_view(), name='invitation-respond'),  # Ответ на приглашение
    path('team-applications/', TeamApplicationCreateView.as_view(), name='team-application-create'),  # Создание заявки команды на участие
    path('team-applications/<int:pk>/response/', TeamApplicationResponseView.as_view(), name='team-application-response'),  # Ответ на заявку команды
    path('user-applications/', UserApplicationCreateView.as_view(), name='user-application-create'),  # Создание пользовательской заявки на участие
    path('user-applications/<int:pk>/response/', ApplicationDecisionView.as_view(), name='user-application-decision'),  # Решение по заявке пользователя
    path('organizer/user/applications/', OrganizerUserApplicationsListView.as_view(), name='organizer-user-applications'),  # Заявки пользователей для организатора
    path('organizer/team/applications/', OrganizerTeamApplicationsListView.as_view(), name='organizer-team-applications'),  # Заявки команд для организатора
    
    # Справочники
    path('faq/', FAQListView.as_view(), name='faq-list'),  # Часто задаваемые вопросы
    path('news/', NewsListView.as_view(), name='news-list'),  # Новости
    path('roles/', RoleListView.as_view(), name='roles-list'),  # Список ролей
    path('regions/', RegionListView.as_view(), name='regions-list'),  # Список регионов
    path('disciplines/', DisciplineListView.as_view(), name='disciplines-list'),  # Список дисциплин
    path('regional-representatives/', RegionalRepresentativesView.as_view(), name='regional-representatives'),  # Региональные представители

]
