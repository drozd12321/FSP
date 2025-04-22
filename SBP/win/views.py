
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (RegisterSerializer, LoginSerializer, TeamCreateSerializer,
CompetitionSerializer, InvitationCreateSerializer, InvitationSerializer, InvitationResponseSerializer,
RoleSerializer,RegionSerializer, TeamApplicationSerializer, TeamApplicationResponseSerializer,
FAQSerializer, NewsSerializer, UserApplicationSerializer, DisciplineSerializer, ApplicationDecisionSerializer,
UserInfoSerializer, VacancyResponseSerializer, ResponseActionSerializer, UserProfileUpdateSerializer,
UserInfoUpdateSerializer, UserUpdateSerializer, ParticipationHistorySerializer, OrganizerCompetitionSerializer,
CompetitionResultsSerializer, UserApprovalSerializer)
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate
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
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Преобразуем название дисциплины в ID если нужно
        if 'discipline' in request.data and isinstance(request.data['discipline'], str):
            logger.debug('1')
            try:
                discipline = Discipline.objects.get(name=request.data['discipline'])
                logger.info(f'Discipline found: {discipline}')

                request.data['discipline'] = discipline.id
            except Discipline.DoesNotExist:
                return Response(
                    {"discipline": "Discipline not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeamCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logger.debug(request.user.id)
            captain = UserInfo.objects.get(user=request.user.id)
            logger.debug(captain)
        except UserInfo.DoesNotExist:
            return Response(
                {"error": "user_profile_incomplete", "detail": "Профиль пользователя не заполнен"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TeamCreateSerializer(
            data=request.data,
            context={'captain': captain}
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        competition = serializer.validated_data['competition']
        captain_region_id = captain.region.id if captain.region else None

        if competition.permissions and isinstance(competition.permissions, list):
            if captain_region_id not in competition.permissions:
                allowed_regions = Region.objects.filter(
                    id__in=competition.permissions
                ).values_list('name', flat=True)
                
                return Response(
                    {
                        "error": "regional_restriction",
                        "detail": f"Регион капитана не разрешен для этого соревнования",
                        "allowed_regions": list(allowed_regions)
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        try:
            team = serializer.save()
            return Response({
                "team_id": team.id,
                "name": team.name,
                "description": team.description,
                "competition_id": team.competition,
                "captain_id": team.captain,
                "is_private": team.is_private,
                "max_members": team.max_members,
                "current_members": team.current_members  # Добавляем текущее количество участников
            }, status=status.HTTP_201_CREATED)
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
    queryset = Competition.objects.all().select_related(
        'discipline',
        'dates'
    )
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FAQListView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = StandardResultsSetPagination
    
class NewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsListView(ListAPIView):
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
        
class OrganizerApplicationsListView(ListAPIView):
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
            'captain'
        ).prefetch_related(
            'members'
        ).annotate(
            members_count=Count('members')
        ).order_by('-created_at')
        
        data = []
        for team in teams:
            team_data = {
                'id': team.id,
                'name': team.name,
                'description': team.description,
                'competition': team.competition,
                'captain': team.captain,
                'max_members': team.max_members,
                'current_members': team.current_members,
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
        serializer = VacancyResponseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Автоматически подставляем текущего пользователя
            serializer.save(user=request.user)
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
        
        # Проверяем, что текущий пользователь - капитан команды
        if request.user.id != team.captain:
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
        user = request.user.id
        user_info = get_object_or_404(UserInfo, user=user)
        
        # Сериализуем данные пользователя
        user_serializer = UserUpdateSerializer(user)
        
        # Сериализуем данные профиля с регионом
        info_serializer = UserInfoUpdateSerializer(user_info)
        
        # Получаем данные региона
        region = user_info.region
        region_serializer = RegionSerializer(region) if region else None
        
        response_data = {
            'user': user_serializer.data,
            'info': info_serializer.data
        }
        
        # Добавляем название региона в ответ
        if region_serializer:
            response_data['info']['region_name'] = region_serializer.data['name']
        
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
        # Получаем UserInfo текущего пользователя
        try:
            user_info = UserInfo.objects.get(user=request.user.id)
        except UserInfo.DoesNotExist:
            return Response(
                {"detail": "Профиль пользователя не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Получаем все участия пользователя
        participations = CompetitionParticipant.objects.filter(
            participant=user_info
        )
        
        # Сериализуем данные
        serializer = ParticipationHistorySerializer(participations, many=True)
        
        # Считаем статистику
        stats = {
            'total_participations': participations.count(),
            'wins': participations.filter(result=1).count(),
            'podiums': participations.filter(result__lte=3).count(),
        }
        
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
            'count': organizers.count(),
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