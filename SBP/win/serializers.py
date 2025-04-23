# users/serializers.py
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from datetime import date
import logging

logger = logging.getLogger(__name__)


class UserApprovalSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    email = serializers.EmailField(source='user.email')
    nickName = serializers.CharField(source='user.nickName')
    role_name = serializers.CharField(source='role.name')
    region_name = serializers.CharField(source='region.name')
    
    class Meta:
        model = UserInfo
        fields = ['user_id', 'email', 'nickName', 'surname', 'name', 'patronymic', 
                 'role_name', 'region_name', 'birthday']

class UserInfoSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())

    class Meta:
        model = UserInfo
        fields = ['surname', 'name', 'patronymic', 'region', 'role', 'birthday', 'is_approved']
        read_only_fields = ['is_approved']  # Поле только для чтения, нельзя установить при регистрации

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    info = UserInfoSerializer()
    
    class Meta:
        model = User
        fields = ['email', 'nickName', 'password', 'info']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value
        
    def validate_nickName(self, value):
        if User.objects.filter(nickName=value).exists():
            raise serializers.ValidationError("Пользователь с таким nickName уже существует")
        return value
    
    def create(self, validated_data):
        info_data = validated_data.pop('info')
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        role = info_data.pop('role')
        # Автоматически подтверждаем, если роль 0
        is_approved = role.id == 0
        UserInfo.objects.create(
            user=user, 
            role=role, 
            is_approved=is_approved,
            **info_data
        )

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                pass
        else:
            try:
                user = User.objects.get(nickName=username)
            except User.DoesNotExist:
                pass

        if user is None:
            raise serializers.ValidationError('Пользователь не найден')

        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')

        if not user.is_active:
            raise serializers.ValidationError('Пользователь не активен')

        # Проверяем подтверждение только для ролей 1 и 2
        if user.info.role.id in [1, 2] and not user.info.is_approved:
            raise serializers.ValidationError('Аккаунт ожидает подтверждения администратором')

        data['user'] = user
        return data
    
class CompetitionDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionDate
        fields = [
            'registration_start',
            'registration_end',
            'start_date',
            'end_date',
        ]

    def validate(self, data):
        if data['registration_start'] >= data['registration_end']:
            raise serializers.ValidationError(
                "Дата окончания регистрации должна быть позже начала."
            )
        
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError(
                "Дата окончания проведения должна быть позже начала."
            )
        
        if data['registration_end'] > data['start_date']:
            raise serializers.ValidationError(
                "Регистрация должна закрываться до начала проведения."
            )
        
        return data
    
class TeamCreateSerializer(serializers.ModelSerializer):
    competition = serializers.PrimaryKeyRelatedField(
        queryset=Competition.objects.filter(type='team'),
        write_only=True
    )

    class Meta:
        model = Team
        fields = ['competition', 'name', 'description', 'is_private']
        extra_kwargs = {
            'name': {'required': True, 'max_length': 100},
            'description': {'required': False, 'allow_blank': True},
            'is_private': {'required': False, 'default': False}
        }

    def validate(self, data):
        request = self.context['request']
        try:
            creator = UserInfo.objects.get(user=request.user)
        except UserInfo.DoesNotExist:
            raise serializers.ValidationError(
                "Профиль пользователя не заполнен. Заполните профиль перед созданием команды."
            )

        competition = data['competition']
        
        if competition.teams.count() >= competition.max_participants:
            raise serializers.ValidationError("Достигнуто максимальное количество команд")
            
        # Если permissions пустые и создатель не модератор
        if competition.permissions == [] and creator.role != 1:
            raise serializers.ValidationError(
                "Создание команд для этого соревнования разрешено только модераторам"
            )
            
        # Проверка региональных ограничений (если permissions не пустые)
        if competition.permissions and competition.permissions != []:
            if not creator.region or creator.region.id not in competition.permissions:
                raise serializers.ValidationError(
                    f"Ваш регион не разрешен для этого соревнования. Разрешены: {competition.permissions}"
                )
        
        return data

    def create(self, validated_data):
        request = self.context['request']
        creator = UserInfo.objects.get(user=request.user)
        
        # Определяем капитана
        captain_id = request.data.get('captain_id')
        if captain_id:
            try:
                captain = UserInfo.objects.get(id=captain_id)
            except UserInfo.DoesNotExist:
                raise serializers.ValidationError("Указанный капитан не найден")
        else:
            captain = creator if creator.role != 1 else None
            # Если капитан не указан и создатель не модератор, назначаем создателя капитаном
            if not captain:
                raise serializers.ValidationError("Для модератора необходимо указать captain_id")

        # Создаем команду
        team = Team.objects.create(
            captain=captain,
            **validated_data
        )
        
        # Добавляем капитана в members (если это не модератор)
        if creator.role != 1 or captain_id:
            if captain and captain not in team.members:
                team.members.append(captain)
                team.save()
        
        return team

    def create(self, validated_data):
        request = self.context['request']
        captain = UserInfo.objects.get(user=request.user)
        competition = validated_data['competition']
        
        # Сначала создаем команду без members
        team = Team.objects.create(
            captain=captain,
            competition=competition,
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            is_private=validated_data.get('is_private', False),
            max_members=competition.max_participants_in_team,
            current_members=1
        )
        
        # Затем добавляем капитана в members
        team.members.add(captain)
        team.save()  # Сохраняем обновленный current_members
        
        return team
        
class InvitationCreateSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserInfo.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = Invitation
        fields = ['team_id', 'user_id']
        extra_kwargs = {
            'team_id': {'required': True},
            'user_id': {'required': True},
        }

    def validate(self, data):
        team = data['team']
        user = data['user']
        request = self.context['request']

        # Проверка что пользователь не капитан
        if team.captain == user.id:
            raise serializers.ValidationError(
                "Нельзя приглашать капитана команды"
            )

        # Проверка что пользователь не уже в команде
        if team.members.filter(id=user.id).exists():
            raise serializers.ValidationError(
                "Пользователь уже в команде"
            )

        # Проверка существующих приглашений
        if Invitation.objects.filter(team=team, user=user, status='Ожидает').exists():
            raise serializers.ValidationError(
                "Приглашение уже отправлено"
            )

        # Проверка что не приглашаем себя
        if user.user == request.user:
            raise serializers.ValidationError(
                "Нельзя приглашать самого себя"
            )

        return data

    def create(self, validated_data):
        # Создаем приглашение со статусом "Ожидает"
        return Invitation.objects.create(
            **validated_data,
            status='Ожидает'
        )
        
class InvitationSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='team.id')
    team_name = serializers.CharField(source='team.name')
    competition_name = serializers.CharField(source='team.competition.name')
    user_nickname = serializers.CharField(source='user.nickName')  # Исправлено на nickName
    
    class Meta:
        model = Invitation
        fields = [
            'id',
            'team_id',
            'team_name',
            'competition_name',
            'user_nickname',
            'status',
        ]
        read_only_fields = fields
    
class InvitationResponseSerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(
        choices=['accept', 'reject'],
        write_only=True,
        required=True
    )

    class Meta:
        model = Invitation
        fields = ['action', 'status']
        read_only_fields = ['id', 'team', 'user']

    def validate(self, attrs):
        if self.instance.status != 'Ожидает':
            raise serializers.ValidationError(
                "Можно ответить только на приглашения со статусом 'Ожидает'"
            )
        return attrs

    def update(self, instance, validated_data):
        action = validated_data['action']
        team = instance.team
        
        if action == 'accept':
            # Проверка максимального количества участников
            if team.members.count() >= team.competition.max_participants:
                raise serializers.ValidationError(
                    f"Команда уже достигла максимального количества участников ({team.competition.max_participants})"
                )
            
            # Проверка что пользователь не уже в команде
            if team.members.filter(id=instance.user).exists():
                raise serializers.ValidationError(
                    "Вы уже состоите в этой команде"
                )
            
            team.members.add(instance.user)
            instance.status = 'Принято'
        else:
            instance.status = 'Отклонено'
        
        instance.save()
        return instance
    
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name'] 
        

        
class TeamApplicationSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        write_only=True
    )

    class Meta:
        model = TeamApplication
        fields = ['team_id', 'status', 'reason']
        extra_kwargs = {
            'team_id': {'required': True}
        }

    def validate(self, attrs):
        # Проверяем, что команда существует
        team = attrs.get('team')
        if not team:
            raise serializers.ValidationError("Команда не найдена")
        
        # Проверяем, что у пользователя есть права на создание заявки для этой команды
        user = self.context['request'].user
        if not team.members.filter(user=user).exists():
            raise serializers.ValidationError("Вы не являетесь участником этой команды")
        
        return attrs

    def create(self, validated_data):
        team = validated_data['team']
        
        # Удаляем все приглашения для этой команды
        Invitation.objects.filter(team=team).delete()
        # Устанавливаем статус "На модерации" и пустое поле reason
        return TeamApplication.objects.create(
            status='pending',
            reason=None,
            **validated_data
        )
        
class TeamApplicationResponseSerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(
        choices=['approve', 'reject'],
        write_only=True,
        required=True
    )
    reason = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = TeamApplication
        fields = ['action', 'reason', 'status']
        read_only_fields = ['id', 'team']

    def validate(self, attrs):
        if self.instance.status != 'pending':
            raise serializers.ValidationError(
                "Можно обрабатывать только заявки со статусом 'pending'"
            )
        
        if attrs['action'] == 'reject' and not attrs.get('reason'):
            raise serializers.ValidationError(
                "При отклонении заявки необходимо указать причину"
            )
        
        return attrs

    def update(self, instance, validated_data):
        action = validated_data['action']
        
        if action == 'approve':
            # Добавляем всех участников команды в соревнование
            for member in instance.team.members.all():
                CompetitionParticipant.objects.get_or_create(
                    competition=instance.team.competition,
                    participant=member
                )
            
            instance.status = 'Одобрено'
            instance.reason = None
            instance.team.save()
        else:
            instance.status = 'Отклонено'
            instance.reason = validated_data['reason']
        
        instance.save()
        return instance
    

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'name']

        
class CompetitionSerializer(serializers.ModelSerializer):
    dates = CompetitionDateSerializer()
    discipline = serializers.PrimaryKeyRelatedField(queryset=Discipline.objects.all())
    discipline_name = serializers.CharField(source='discipline.name', read_only=True)
    permissions_status = serializers.SerializerMethodField()  # Новое поле
    # остальные поля остаются без изменений
    competition_type_display = serializers.CharField(
        source='get_competition_type_display',
        read_only=True
    )
    type_display = serializers.CharField(
        source='get_type_display',
        read_only=True
    )

    class Meta:
        model = Competition
        fields = [
            'id',
            'name',
            'discipline',
            'discipline_name',  # добавляем поле для отображения названия
            'description',
            'max_participants',
            'max_participants_in_team',
            'min_age',
            'max_age',
            'competition_type',
            'competition_type_display',
            'type',
            'type_display',
            'status',
            'permissions',
            'dates',
            'permissions_status',  # Добавляем новое поле
        ]

    def get_permissions_status(self, obj):
        if not obj.permissions:  # Если permissions пустое
            return 0
        elif len(obj.permissions) != 89:  # Если длина permissions не равна 89
            return 1
        else:  # Если длина permissions равна 89
            return 2

    def create(self, validated_data):
        dates_data = validated_data.pop('dates')

        
        competition = Competition.objects.create(**validated_data)

        
        CompetitionDate.objects.create(
            competition=competition,
            **dates_data
        )
        
        return competition
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']
        read_only_fields = ['id']
        
class NewsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'content',
            'image_url',
            'date'
        ]
        read_only_fields = fields

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    def get_date(self, obj):
        return obj.created_at.strftime("%d.%m.%Y")
    
class UserDisciplineStatsSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()
    
    class Meta:
        model = UserDisciplineStats
        fields = ['discipline', 'competitions_count', 'points_count']
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']
        
class UserApplicationSerializer(serializers.ModelSerializer):
    competition = serializers.PrimaryKeyRelatedField(
        queryset=Competition.objects.filter(type='individual')
    )
    
    class Meta:
        model = UserApplication
        fields = ['id', 'competition', 'status', 'reason']

    def validate(self, data):
        competition = data['competition']
        user = self.context['request'].user
        
        # Получаем информацию о пользователе
        try:
            user_info = UserInfo.objects.get(user=user)
        except UserInfo.DoesNotExist:
            raise serializers.ValidationError("Профиль пользователя не найден")

        # 1. Проверка возрастных ограничений
        today = date.today()
        age = today.year - user_info.birthday.year - ((today.month, today.day) < 
                                                     (user_info.birthday.month, user_info.birthday.day))
        
        if age < competition.min_age or age > competition.max_age:
            raise serializers.ValidationError(
                f"Возрастные ограничения: от {competition.min_age} до {competition.max_age} лет"
            )

        # 2. Проверка региональных ограничений
        if hasattr(competition, 'permissions') and isinstance(competition.permissions, list):
            if user_info.region.id not in competition.permissions:
                allowed_regions = Region.objects.filter(
                    id__in=competition.permissions
                ).values_list('name', flat=True)
                
                raise serializers.ValidationError({
                    "regional_restriction": {
                        "message": "Ваш регион не участвует в этом соревновании",
                        "user_region": user_info.region.name,
                        "allowed_regions": list(allowed_regions)
                    }
                })

        # 3. Проверка существующей заявки
        if UserApplication.objects.filter(user=user_info, competition=competition).exists():
            raise serializers.ValidationError(
                "Вы уже подавали заявку на это соревнование"
            )

        # 4. Проверка что соревнование действительно индивидуальное
        if competition.type != 'individual':
            raise serializers.ValidationError(
                "Заявки подаются только на индивидуальные соревнования"
            )

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        user_info = UserInfo.objects.get(user=user)
        return UserApplication.objects.create(
            user=user_info,
            **validated_data
        )
        
class ApplicationDecisionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'], required=True)
    reason = serializers.CharField(required=False, allow_blank=True)
    
class UserInfoSerializer(serializers.ModelSerializer):
    nickName = serializers.CharField(source='user.nickName')  # Доступ к полю из связанной модели User
    class Meta:
        model = UserInfo
        fields = ['surname', 'name', 'nickName', 'rating']
        
class VacancyResponseSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    user_surname = serializers.CharField(source='user.surname', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_nickname = serializers.CharField(source='user.user.nickName', read_only=True)
    
    # Поля для ввода (клиентские имена)
    id = serializers.IntegerField(write_only=True)  # Будет преобразовано в team.id
    description = serializers.CharField(write_only=True)  # Будет преобразовано в text

    class Meta:
        model = VacancyResponse
        fields = [
            'id',          # write_only (из запроса)
            'description', # write_only (из запроса)
            'text',        # read_only (для ответа)
            'status', 
            'team',       # read_only (для ответа)
            'team_name', 
            'user',
            'user_surname',
            'user_name',
            'user_nickname'
        ]
        read_only_fields = ['status', 'team', 'text', 'team_name', 
                          'user_surname', 'user_name', 'user_nickname']

    def create(self, validated_data):
        # Извлекаем специальные поля
        team_id = validated_data.pop('id')
        text_content = validated_data.pop('description')
        
        # Получаем объект команды
        team = Team.objects.get(id=team_id)
        
        # Создаем объект отклика
        return VacancyResponse.objects.create(
            team=team,
            text=text_content,
            **validated_data
        )
        
class ResponseActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['accept', 'reject'])
    response_id = serializers.IntegerField()
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'nickName']
        extra_kwargs = {
            'email': {'required': False},
            'nickName': {'required': False}
        }

class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['surname', 'name', 'patronymic', 'region', 'role', 'birthday',  'user_id']
        extra_kwargs = {
            'region': {'required': False},
            'role': {'required': False},
            'birthday': {'required': False}
        }

class UserProfileUpdateSerializer(serializers.Serializer):
    user = UserUpdateSerializer(required=False)
    info = UserInfoUpdateSerializer(required=False)
    
class CompetitionShortSerializer(serializers.ModelSerializer):
    discipline = serializers.CharField(source='discipline.name')
    
    class Meta:
        model = Competition
        fields = ['id', 'name', 'discipline', 'type']

class ParticipationHistorySerializer(serializers.ModelSerializer):
    competition = CompetitionShortSerializer()
    
    class Meta:
        model = CompetitionParticipant
        fields = ['competition', 'result']
        
class OrganizerCompetitionSerializer(serializers.ModelSerializer):
    competition = serializers.SerializerMethodField()
    rated = serializers.BooleanField(source='rated')
    
    class Meta:
        model = CompetitionOrganizer
        fields = ['competition', 'rated']
    
    def get_competition(self, obj):
        competition = obj.competition
        discipline_name = Discipline.objects.get(id = competition.discipline).name
        return {
            'id': competition.id,
            'name': competition.name,
            'discipline': discipline_name,
            'type': competition.type,
            'status': competition.status
        }
        
class ResultDistributionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    result = serializers.IntegerField(min_value=1)

class CompetitionResultsSerializer(serializers.Serializer):
    competition_id = serializers.IntegerField()
    results = ResultDistributionSerializer(many=True)
    
class MemberNicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickName']

class TeamListSerializer(serializers.ModelSerializer):
    competition_name = serializers.CharField(source='competition.name')
    competition_status = serializers.CharField(source='competition.status')
    discipline_name = serializers.CharField(source='competition.discipline.name')  # Новое поле
    members = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 
            'name', 
            'competition_name', 
            'competition_status',
            'discipline_name',  # Добавлено новое поле
            'members',
            'captain',
        ]
    
    def get_members(self, obj):
        # Оптимизация запроса с select_related
        members = obj.members.all().select_related('user')
        return [{
            'id': member.user.id,
            'nickName': member.user.nickName
        } for member in members]
        
class CompetitionDecisionSerializer(serializers.Serializer):
    competition_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['accept', 'reject'])
    
class IndividualParticipantSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    nickName = serializers.CharField(source='user.user.nickName')
    name = serializers.CharField(source='user.name')
    surname = serializers.CharField(source='user.surname')
    
    class Meta:
        model = UserApplication
        fields = ['user_id', 'nickName', 'name', 'surname', 'status']

class TeamParticipantSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='team.id')
    team_name = serializers.CharField(source='team.name')
    captain_name = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamApplication
        fields = ['team_id', 'team_name', 'captain_name', 'members', 'status']
    
    def get_captain_name(self, obj):
        return f"{obj.team.captain.surname} {obj.team.captain.name}"
    
    def get_members(self, obj):
        return [
            {
                'user_id': member.user.id,
                'nickName': member.user.nickName,
                'name': member.name,
                'surname': member.surname
            } for member in obj.team.members.all()
        ]
        
        
class RegionalRepresentativeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    region_name = serializers.CharField(source='region.name')
    
    class Meta:
        model = UserInfo
        fields = ['surname', 'name', 'patronymic', 'email', 'region_name']
        
class TeamWithCompetitionSerializer(serializers.ModelSerializer):
    competition = CompetitionShortSerializer()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'competition']

class UserVacancyResponseSerializer(serializers.ModelSerializer):
    team = TeamWithCompetitionSerializer()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = VacancyResponse
        fields = ['id', 'text', 'status', 'status_display', 'team', 'created_at']