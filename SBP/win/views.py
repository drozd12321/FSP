
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (RegisterSerializer, LoginSerializer, TeamCreateSerializer,
CompetitionSerializer, InvitationCreateSerializer, InvitationSerializer, InvitationResponseSerializer,
RoleSerializer,RegionSerializer, TeamApplicationSerializer, TeamApplicationResponseSerializer,
FAQSerializer, NewsSerializer, UserApplicationSerializer, DisciplineSerializer, ApplicationDecisionSerializer,
UserInfoSerializer)
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
import logging
logger = logging.getLogger(__name__)
class RegisterView(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            token, created = Token.objects.get_or_create(user=user)
            
            role = user.info.role
            role_serializer = RoleSerializer(role)
            
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
            captain = UserInfo.objects.get(id=request.user.id)
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