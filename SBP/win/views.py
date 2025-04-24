
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.authtoken.models import Token 
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.db import transaction
import logging
from django.db.models import Count
logger = logging.getLogger(__name__)

class UserApprovalView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Проверяем, что текущий пользователь имеет право подтверждать других (role=2)
        if request.user.info.role.id != 2:
            return Response({'error': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
        
        # Получаем список пользователей, ожидающих подтверждения (role 1 или 2)
        pending_users = UserInfo.objects.filter(
            role__id__in=[1, 2],
            is_approved=False
        ).select_related('user', 'role', 'region')
        
        serializer = UserApprovalSerializer(pending_users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Проверяем права
        if request.user.info.role.id != 2:
            return Response({'error': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        action = request.data.get('action')  # 'approve' или 'reject'
        
        try:
            user_info = UserInfo.objects.get(user__id=user_id)
        except UserInfo.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        if action == 'approve':
            user_info.is_approved = True
            user_info.save()
            return Response({'message': 'Пользователь успешно подтвержден'})
        elif action == 'reject':
            # Можно добавить логику удаления или просто оставить неподтвержденным
            user_info.user.delete()  # или user_info.delete()
            return Response({'message': 'Пользователь отклонен и удален'})
        else:
            return Response({'error': 'Неверное действие'}, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterView(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Для ролей 1 и 2 не создаем токен и не логиним
            if user.info.role.id in [1, 2]:
                return Response({
                    'message': 'Регистрация успешна. Ожидайте подтверждения администратором.'
                }, status=status.HTTP_201_CREATED)
            else:
                # Для роли 0 сразу выдаем токен
                token, created = Token.objects.get_or_create(user=user)
                role_serializer = RoleSerializer(user.info.role)
                
                return Response({
                    'message': 'Пользователь успешно зарегистрирован',
                    'token': token.key,
                    'role': role_serializer.data
                }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)
        
        # Сериализуем данные пользователя
        user_info = user.info
        role_serializer = RoleSerializer(user_info.role)
        
        return Response({
            'token': token.key,
            'role': role_serializer.data,
            'user': {
                'id': user.id,
                'email': user.email,
                'nickName': user.nickName,
                'info': {
                    'name': user_info.name,
                    'surname': user_info.surname
                }
            }
        })
    
class CompetitionCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Преобразуем название дисциплины в ID если нужно
        if 'discipline' in request.data and isinstance(request.data['discipline'], str):
            try:
                discipline = Discipline.objects.get(name=request.data['discipline'])
                request.data['discipline'] = discipline.id
            except Discipline.DoesNotExist:
                return Response(
                    {"discipline": "Discipline not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Обрабатываем permissions - преобразуем в список ID
        if 'permissions' in request.data and isinstance(request.data['permissions'], list):
            try:
                # Извлекаем только ID из объектов регионов
                permissions_data = request.data['permissions']
                region_ids = [item['id'] for item in permissions_data if isinstance(item, dict) and 'id' in item]
                request.data['permissions'] = region_ids
            except (TypeError, KeyError):
                return Response(
                    {"permissions": "Invalid format - expected list of regions with ids"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            competition = serializer.save()
            
            # Получаем UserInfo текущего пользователя
            try:
                user_info = UserInfo.objects.get(user=request.user)
            except UserInfo.DoesNotExist:
                return Response(
                    {"error": "User profile not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Создаем запись организатора
            CompetitionOrganizer.objects.create(
                user=user_info,  # Передаем экземпляр UserInfo
                competition=competition,
                rated=False
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeamCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TeamCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            team = serializer.save()
            return Response({
                "team_id": team.id,
                "name": team.name,
                "competition_id": team.competition.id,
                "captain_id": team.captain.id,
                "max_members": team.max_members
            }, status=status.HTTP_201_CREATED)
        except UserInfo.DoesNotExist:
            return Response(
                {"error": "profile_incomplete", "detail": "Профиль пользователя не заполнен"},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"error": "creation_error", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class InvitationCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InvitationCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Проверяем что текущий пользователь - капитан команды
            team = serializer.validated_data['team']
            if team.captain != request.user.id:
                return Response(
                    {"detail": "Только капитан команды может отправлять приглашения"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            invitation = serializer.save()
            return Response({
                'id': invitation.id,
                'team_id': invitation.team.id,
                'user_id': invitation.user.id,
                'status': invitation.status
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserInvitationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        invitations = Invitation.objects.filter(
            user=request.user.id,
            status='Ожидает'
        )
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)
    
class InvitationResponseView(UpdateAPIView):
    serializer_class = InvitationResponseSerializer
    permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей
    queryset = Invitation.objects.all()
    http_method_names = ['patch']

    def get_object(self):
        try:
            invitation = super().get_object()
            # Проверяем что пользователь отвечает на свое приглашение
            if invitation.user != self.request.user.id:
                raise PermissionDenied("Вы можете отвечать только на свои приглашения")
            return invitation
        except Invitation.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND("Приглашение не найдено")

class RegionListView(ListAPIView):
    queryset = Region.objects.all().order_by('id')
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]
    
class RoleListView(ListAPIView):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
    
class TeamApplicationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TeamApplicationSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            application = serializer.save()
            return Response({
                'id': application.id,
                'team_id': application.team.id,
                'status': application.status,
                'reason': application.reason
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeamApplicationResponseView(UpdateAPIView):
    serializer_class = TeamApplicationResponseSerializer
    permission_classes = [IsAuthenticated]
    queryset = TeamApplication.objects.all()
    http_method_names = ['patch']

    def perform_update(self, serializer):   
        serializer.save()
        
class CompetitionListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.exclude(status='pending').select_related(
        'discipline',
        'dates'
    )
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FAQListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = StandardResultsSetPagination
    
class NewsPagination(PageNumberPagination):
    permission_classes = [AllowAny]
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    pagination_class = NewsPagination
    search_fields = ['title', 'content']
    
class UserApplicationCreateView(CreateAPIView):
    serializer_class = UserApplicationSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserApplication.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError("Вы уже подавали заявку на это соревнование")

class DisciplineListView(ListAPIView):
    queryset = Discipline.objects.all().order_by('id')
    serializer_class = DisciplineSerializer
    permission_classes = [AllowAny]
    
class ApplicationDecisionView(UpdateAPIView):
    serializer_class = ApplicationDecisionSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserApplication.objects.all()

    def get_object(self):
        application = get_object_or_404(UserApplication, pk=self.kwargs['pk'])
        user_info = self.request.user
        
        # Проверяем что пользователь организатор этого соревнования
        if not CompetitionOrganizer.objects.filter(
            user=user_info.id,
            competition=application.competition
        ).exists():
            raise PermissionDenied("Вы не являетесь организатором этого соревнования")
        
        return application

    def perform_update(self, serializer):
        application = self.get_object()
        action = serializer.validated_data['action']
        reason = serializer.validated_data.get('reason', '')

        if action == 'approve':
            if application.competition.participants.count() >= application.competition.max_participants:
                raise ValidationError("Достигнуто максимальное количество участников")
            
        if action == 'approve':
            application.status = 'approved'
            application.reason = None
            # Создаем запись об участии
            CompetitionParticipant.objects.get_or_create(
                competition=application.competition,
                participant=application.user
            )
        else:
            application.status = 'rejected'
            application.reason = reason
        
        application.save()
        
class OrganizerUserApplicationsListView(ListAPIView):
    serializer_class = UserApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_info = self.request.user
        # Получаем соревнования, где пользователь организатор
        organized_competitions = CompetitionOrganizer.objects.filter(
            user=user_info.id
        ).values_list('competition', flat=True)
        
        return UserApplication.objects.filter(
            competition__in=organized_competitions,
            status='pending'
        ).select_related('user','competition')

class UserListView(ListAPIView):
    queryset = UserInfo.objects.filter(role_id=0).order_by('id')  # Фильтр по role_id=0
    serializer_class = UserInfoSerializer
    permission_classes = [AllowAny]
    

class PublicTeamsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        teams = Team.objects.filter(is_private=False).select_related(
            'competition', 
            'captain',
            'captain__user',  # Добавляем связь с пользователем капитана
            'competition__dates'  # Добавляем связь с датами соревнования
        ).prefetch_related(
            'members'
        ).annotate(
            members_count=Count('members')
        )
        
        data = []
        for team in teams:
            team_data = {
                'id': team.id,
                'name': team.name,
                'description': team.description,
                'competition': {
                    'id': team.competition.id,
                    'name': team.competition.name,
                    'dates': {
                        'start_date': team.competition.dates.start_date if hasattr(team.competition, 'dates') else None,
                        'end_date': team.competition.dates.end_date if hasattr(team.competition, 'dates') else None,
                        'registration_start': team.competition.dates.registration_start if hasattr(team.competition, 'dates') else None,
                        'registration_end': team.competition.dates.registration_end if hasattr(team.competition, 'dates') else None,
                    }
                },
                'captain': {
                    'id': team.captain.id if team.captain else None,
                    'nickName': team.captain.user.nickName if team.captain and hasattr(team.captain, 'user') else None
                },
                'max_members': team.max_members,
                'current_members': team.members_count,  # Используем аннотированное значение
                'is_private': team.is_private,
                'members_count': team.members_count  # Дублируем для совместимости
            }
            data.append(team_data)
        
        return Response({
            'count': len(data),
            'teams': data
        }, status=status.HTTP_200_OK)
        
class CaptainVacancyResponsesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Проверяем, является ли пользователь капитаном какой-либо команды
        user_teams = Team.objects.filter(captain=request.user.id)
        
        if not user_teams.exists():
            return Response(
                {"error": "not_a_captain", "detail": "Вы не являетесь капитаном ни одной команды"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Получаем все отклики для команд пользователя-капитана
        responses = VacancyResponse.objects.filter(
            team__in=user_teams.values_list('id', flat=True)
        ).select_related('team')  # Оптимизация запросов к БД

        serializer = VacancyResponseSerializer(responses, many=True)
        
        return Response({
            'count': responses.count(),
            'responses': serializer.data
        }, status=status.HTTP_200_OK)
        
class ResponseToPublicView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_info = UserInfo.objects.get(user=request.user)
        except UserInfo.DoesNotExist:
            return Response(
                {"detail": "Профиль пользователя не найден"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Добавляем user_info в данные для сериализатора
        request.data['user'] = user_info.id
        
        serializer = VacancyResponseSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResponseActionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ResponseActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        response = get_object_or_404(VacancyResponse, id=serializer.validated_data['response_id'])
        team = response.team
        logger.debug(f'response : {response}')
        logger.debug(f"team : {team}")
        logger.debug(f'team captain : {team.captain.id}')
        logger.debug(f'request.user.id : {request.user.id}')
        # Проверяем, что текущий пользователь - капитан команды
        if request.user.id != team.captain.id:
            return Response(
                {"detail": "Только капитан команды может обрабатывать заявки"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        action = serializer.validated_data['action']
        
        if action == 'accept':
            # Проверяем, есть ли место в команде
            if team.current_members >= team.max_members:
                return Response(
                    {"detail": "В команде нет свободных мест"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Добавляем пользователя в команду
            team.members.add(response.user)
            team.current_members = team.members.count()
            team.save()
            
            # Обновляем статус заявки
            response.status = VacancyResponse.ACCEPTED
            response.save()
            
            return Response(
                {"detail": "Заявка принята, пользователь добавлен в команду"},
                status=status.HTTP_200_OK
            )
        
        elif action == 'reject':
            response.status = VacancyResponse.REJECTED
            response.save()
            
            return Response(
                {"detail": "Заявка отклонена"},
                status=status.HTTP_200_OK
            )
            
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user  # Получаем объект пользователя, а не только ID
        user_info = get_object_or_404(UserInfo, user=user)
        
        # Сериализуем данные пользователя
        user_serializer = UserUpdateSerializer(user)  # Теперь передаем объект пользователя
        
        # Сериализуем данные профиля с регионом
        info_serializer = UserInfoUpdateSerializer(user_info)
        
        # Получаем данные региона
        region = user_info.region
        region_serializer = RegionSerializer(region) if region else None
        
        # Получаем данные роли
        role = user_info.role
        role_serializer = RoleSerializer(role) if role else None
        
        response_data = {
            'user': user_serializer.data,
            'info': info_serializer.data
        }
        
        # Добавляем название региона в ответ
        if region_serializer:
            response_data['info']['region_name'] = region_serializer.data['name']
        
        # Добавляем название роли в ответ
        if role_serializer:
            response_data['info']['role_name'] = role_serializer.data['name']
        
        return Response(response_data)
    
    def patch(self, request):
        # Получаем текущего пользователя и его профиль
        user = request.user
        user_info = get_object_or_404(UserInfo, user=user.id)
        
        # Сериализуем данные
        serializer = UserProfileUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Обновляем данные User
        user_data = serializer.validated_data.get('user', {})
        if user_data:
            user_serializer = UserUpdateSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Обновляем данные UserInfo
        info_data = serializer.validated_data.get('info', {})
        if info_data:
            info_serializer = UserInfoUpdateSerializer(user_info, data=info_data, partial=True)
            if info_serializer.is_valid():
                info_serializer.save()
            else:
                return Response(info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            {"detail": "Данные успешно обновлены"},
            status=status.HTTP_200_OK
        )
        
class ParticipationHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user_info = UserInfo.objects.get(user=request.user.id)
        except UserInfo.DoesNotExist:
            return Response(
                {"detail": "Профиль пользователя не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        participations = CompetitionParticipant.objects.filter(
            participant=user_info
        ).select_related('competition').annotate(
            total_participants=Count('competition__participants')
        )
        
        stats = {
            'total_participations': participations.count(),
            'wins': participations.filter(result=1).count(),
            'podiums': participations.filter(result__lte=3).count(),
            'current_rating': user_info.rating,
        }
        
        serializer = ParticipationHistorySerializer(participations, many=True)
        
        return Response({
            'stats': stats,
            'history': serializer.data
        })
        
class OrganizedCompetitionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Получаем UserInfo текущего пользователя
        user_info = get_object_or_404(UserInfo, user=request.user)
        
        # Получаем все соревнования где пользователь организатор
        organizers = CompetitionOrganizer.objects.filter(
            user=user_info
        ).select_related('competition', 'competition__discipline')
        
        serializer = OrganizerCompetitionSerializer(organizers, many=True)
        
        return Response({
            'competitions': serializer.data
        })
        
class DistributeResultsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = CompetitionResultsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        competition_id = serializer.validated_data['competition_id']
        results_data = serializer.validated_data['results']
        
        # Получаем соревнование
        competition = get_object_or_404(Competition, id=competition_id)
        
        # Проверяем что соревнование завершено
        if competition.status != 'completed':
            return Response(
                {"detail": "Нельзя распределить места для незавершенного соревнования"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем что пользователь организатор этого соревнования
        user_info = get_object_or_404(UserInfo, user=request.user)
        is_organizer = CompetitionOrganizer.objects.filter(
            user=user_info,
            competition=competition
        ).exists()
        
        if not is_organizer:
            return Response(
                {"detail": "Только организатор может распределять места"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Обновляем результаты участников
        for result_data in results_data:
            participant = get_object_or_404(
                CompetitionParticipant,
                competition=competition,
                participant_id=result_data['user']
            )
            participant.result = result_data['result']
            participant.save()
        
        # Помечаем что организатор оценил соревнование
        organizer = CompetitionOrganizer.objects.get(
            user=user_info,
            competition=competition
        )
        organizer.rated = True
        organizer.save()
        
        return Response(
            {"detail": "Места успешно распределены"},
            status=status.HTTP_200_OK
        )
        
class UserTeamsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Оптимизированный запрос с select_related
        user_info = get_object_or_404(UserInfo, user_id=request.user.id)
        
        # Получаем команды с предзагрузкой связанных данных
        teams = Team.objects.filter(
            members=user_info.user_id
        ).select_related(
            'competition',
            'competition__discipline'  # Добавлено для оптимизации
        ).prefetch_related(
            'members',
            'members__user'
        )
        
        logger.debug(f"User ID: {request.user.id}, UserInfo ID: {user_info.id}")
        logger.debug(f"Teams found: {teams.count()}")
        
        serializer = TeamListSerializer(teams, many=True)
        return Response({
            'count': teams.count(),
            'teams': serializer.data
        })
        
class PendingCompetitionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Получаем все соревнования со статусом 'pending'
        competitions = Competition.objects.filter(status='pending').select_related(
            'discipline'
        ).prefetch_related('dates')
        
        serializer = CompetitionSerializer(competitions, many=True)
        
        return Response({
            'competitions': serializer.data
        })
        
class OrganizerTeamApplicationsListView(ListAPIView):
    serializer_class = TeamApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_info = self.request.user
        # Получаем соревнования, где пользователь организатор
        organized_competitions = CompetitionOrganizer.objects.filter(
            user=user_info.id
        ).values_list('competition', flat=True)
        
        return TeamApplication.objects.filter(
            competition__in=organized_competitions,
            status='pending'  # или 'pending' в зависимости от вашей логики
        ).select_related('team', 'competition')
        
class CompetitionDecisionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = CompetitionDecisionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        competition_id = serializer.validated_data['competition']
        action = serializer.validated_data['action']
        
        # Получаем соревнование
        competition = get_object_or_404(Competition, id=competition_id, status='pending')
        
        # Проверяем что пользователь имеет право подтверждать соревнования
        try:
            user_info = UserInfo.objects.get(user=request.user)
            if user_info.role.id != 2:  # Проверка что пользователь модератор
                return Response(
                    {"detail": "Только представители ФСП могут подтверждать соревнования"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except UserInfo.DoesNotExist:
            return Response(
                {"detail": "Профиль пользователя не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if action == 'accept':
            # Обновляем статус соревнования
            competition.status = 'upcoming'
            competition.save()
            
            return Response(
                {"detail": "Соревнование подтверждено", "competition_id": competition.id},
                status=status.HTTP_200_OK
            )
        
        elif action == 'reject':
            # Удаляем записи организаторов
            CompetitionOrganizer.objects.filter(competition=competition).delete()
            
            # Удаляем само соревнование
            competition.delete()
            
            return Response(
                {"detail": "Соревнование отклонено и удалено"},
                status=status.HTTP_200_OK
            )
            
class CompetitionParticipantsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, competition_id):
        competition = get_object_or_404(Competition, id=competition_id)
        
        if competition.type == 'individual':
            # Для индивидуальных соревнований
            participants = UserApplication.objects.filter(
                competition=competition,
                status='approved'
            ).select_related('user__user')
            
            serializer = IndividualParticipantSerializer(participants, many=True)
            
        else:
            # Для командных соревнований
            participants = TeamApplication.objects.filter(
                competition=competition,
                status='approved'
            ).select_related('team__captain').prefetch_related('team__members__user')
            
            serializer = TeamParticipantSerializer(participants, many=True)
        
        return Response({
            'competition_id': competition.id,
            'competition_name': competition.name,
            'competition_type': competition.type,
            'participants': serializer.data
        })
        
class RegionalRepresentativesView(ListAPIView):
    permission_classes = [AllowAny]  # Или [IsAuthenticated] если нужно ограничить доступ
    serializer_class = RegionalRepresentativeSerializer
    
    def get_queryset(self):
        return UserInfo.objects.filter(
            role_id=1,  # Фильтр по role=1 (региональные представители)
            is_approved=True  # Только подтвержденные пользователи
        ).select_related('user', 'region')  # Оптимизация запросов
        
class CompetitionStatusView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Получаем время из запроса
        client_time_str = request.query_params.get('time', None)
        
        if not client_time_str:
            return Response(
                {"error": "Параметр 'time' обязателен в формате ISO 8601 (например, 2025-03-02T21:00:00Z)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            client_time = datetime.fromisoformat(client_time_str.replace('Z', '+00:00'))
            client_time = timezone.make_aware(client_time)
        except ValueError:
            return Response(
                {"error": "Неверный формат времени. Используйте ISO 8601 (например, 2025-03-02T21:00:00Z)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получаем все соревнования с датами
        competitions = Competition.objects.filter(
            dates__isnull=False
        ).select_related('dates').only(
            'id', 'status', 'dates__start_date', 
            'dates__end_date', 'dates__registration_start',
            'dates__registration_end'
        )
        
        updated_competitions = []
        
        for comp in competitions:
            original_status = comp.status
            new_status = original_status
            
            # Если текущий статус pending - не меняем
            if original_status == 'pending':
                updated_competitions.append({
                    'id': comp.id,
                    'name': comp.name,
                    'original_status': original_status,
                    'new_status': new_status,
                    'status_changed': False
                })
                continue
            
            dates = comp.dates
            
            # Определяем новый статус
            if dates.registration_start <= client_time <= dates.registration_end:
                new_status = 'registration'
            elif dates.start_date <= client_time <= dates.end_date:
                new_status = 'running'
            elif client_time > dates.end_date:
                new_status = 'finished'
            else:
                new_status = 'waiting'
            
            # Обновляем если статус изменился
            status_changed = new_status != original_status
            if status_changed:
                comp.status = new_status
                comp.save(update_fields=['status'])
            
            updated_competitions.append({
                'id': comp.id,
                'name': comp.name,
                'original_status': original_status,
                'new_status': new_status,
                'status_changed': status_changed
            })
        
        return Response({
            'client_time': client_time_str,
            'server_time': timezone.now().isoformat(),
            'competitions_updated': len([c for c in updated_competitions if c['status_changed']]),
            'competitions': updated_competitions
        })
        
class UserVacancyResponsesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Получаем UserInfo текущего пользователя
            user_info = request.user.info
        except AttributeError:
            return Response(
                {"detail": "Профиль пользователя не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Получаем все отклики пользователя с предварительной загрузкой связанных данных
        responses = VacancyResponse.objects.filter(
            user=user_info
        ).select_related(
            'team',
            'team__competition'
        ).order_by('-created_at')
        
        serializer = UserVacancyResponseSerializer(responses, many=True)
        
        return Response({
            'count': responses.count(),
            'responses': serializer.data
        })
        
class RegionCompetitionsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, region_id):
        try:
            region_id = int(region_id)  # Преобразуем в число
        except ValueError:
            return Response(
                {"error": "Номер региона должен быть числом"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ищем соревнования, где:
        # 1) region_id есть в permissions
        # 2) статус не 'pending' и не 'finished'
        competitions = Competition.objects.filter(
            permissions__contains=[region_id],
        ).exclude(
            status__in=['pending', 'finished']
        ).select_related('discipline')
        
        serializer = CompetitionShortSerializer(competitions, many=True)
        
        return Response({
            'region_id': region_id,
            'count': competitions.count(),
            'competitions': serializer.data
        })