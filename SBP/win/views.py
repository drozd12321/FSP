
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (RegisterSerializer, LoginSerializer, TeamCreateSerializer,
CompetitionSerializer, InvitationCreateSerializer, InvitationSerializer, InvitationResponseSerializer,
RoleSerializer,RegionSerializer, TeamApplicationSerializer, TeamApplicationResponseSerializer)
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import UpdateAPIView, ListAPIView



class RegisterView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Пользователь успешно зарегистрирован'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Аутентификация пользователя через Django
        user = None
        if '@' in username:
            # Поиск по email
            try:
                from .models import User
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.nickName, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({'detail': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
class CompetitionCreateView(APIView):
    def post(self, request):
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeamCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TeamCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем региональные ограничения
        competition = serializer.validated_data['competition']
        user_region = request.user.userinfo.region
        
        if (hasattr(competition, 'permissions') and 
            'allowed_regions' in competition.permissions and 
            user_region.id not in competition.permissions['allowed_regions']):
            
            allowed_regions = Region.objects.filter(
                id__in=competition.permissions['allowed_regions']
            ).values_list('name', flat=True)
            
            return Response(
                {
                    "detail": (
                        "На региональные соревнования могут создаваться команды только из разрешенных регионов. "
                        f"Допустимые регионы: {', '.join(allowed_regions)}"
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Создаем команду
        serializer.validated_data['creator_id'] = request.user.userinfo
        team = serializer.save()
        
        return Response({
            'id': team.id,
            'name': team.name,
            'competition_id': team.competition.id,
            'captain_id': team.captain.id,
            'members': [team.captain.id],
            'message': 'Команда успешно создана'
        }, status=status.HTTP_201_CREATED)

class InvitationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InvitationCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Проверяем что текущий пользователь - капитан команды
            team = serializer.validated_data['team']
            if team.captain.user != request.user:
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
            user=request.user.userinfo,
            status='Ожидает'
        )
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)
    
class InvitationResponseView(UpdateAPIView):
    serializer_class = InvitationResponseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Invitation.objects.all()
    http_method_names = ['patch']

    def get_object(self):
        invitation = super().get_object()
        # Проверяем, что текущий пользователь - получатель приглашения
        if invitation.user.user != self.request.user:
            raise PermissionDenied("Вы можете отвечать только на свои приглашения")
        return invitation

    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class RegionListView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    
class RoleListView(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
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
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all().select_related(
        'discipline',
        'dates'
    ).prefetch_related('regions')