# users/serializers.py
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from datetime import date

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserInfoSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())  # Принимаем id роли
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())  # Принимаем id региона

    class Meta:
        model = UserInfo
        fields = ['surname', 'name', 'patronymic', 'region', 'role', 'birthday']

        
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

        role = info_data.pop('role')  # теперь это объект Role
        UserInfo.objects.create(user=user, role=role, **info_data)

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # может быть email или nickName
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Попытка найти пользователя по nickName или email
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
        source='competition',
        write_only=True
    )
    captain_id = serializers.IntegerField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Team
        fields = ['competition', 'name', 'captain', 'is_private']  # Добавлено is_private
        extra_kwargs = {
            'name': {'required': True, 'max_length': 100},
            'is_private': {'required': False}  # Необязательное поле, по умолчанию False
        }

    def validate(self, data):
        competition = data['competition']
        if competition.participant.count() >= competition.max_participants:
            raise serializers.ValidationError(
                "Достигнуто максимальное количество команд"
            )
        return data

    def create(self, validated_data):
        captain = self.context.get('captain')
        if not captain:
            raise serializers.ValidationError("Не указан капитан команды")
            
        team = Team.objects.create(
            captain=captain,
            competition=validated_data['competition'],
            name=validated_data['name'],
            is_private=validated_data.get('is_private', False)  # Учитываем is_private
        )
        team.members.add(captain)
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
        fields = '__all__'  # или конкретные поля, например ['id', 'name', 'code']
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'  # или конкретные поля
        
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
            status='На модерации',
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
        if self.instance.status != 'На модерации':
            raise serializers.ValidationError(
                "Можно обрабатывать только заявки со статусом 'На модерации'"
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
            'dates'
        ]

    def create(self, validated_data):
        dates_data = validated_data.pop('dates')
        
        # discipline уже будет объектом, так как использовали PrimaryKeyRelatedField
        competition = Competition.objects.create(**validated_data)
        
        # Создаем даты для соревнования
        CompetitionDate.objects.create(competition=competition, **dates_data)
        
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
        

class UserApplicationSerializer(serializers.ModelSerializer):
    competition_id = serializers.PrimaryKeyRelatedField(
        queryset=Competition.objects.filter(type='individual'),
        source='competition',
        write_only=True
    )
    
    class Meta:
        model = UserApplication
        fields = ['id', 'competition_id', 'status', 'reason']

    def validate(self, data):
        competition = data['competition']
        user_info = self.context['request'].user
        user_region = UserInfo.objects.filter(id = user_info.id).region

        # 1. Проверка возрастных ограничений
        today = date.today()
        age = today.year - (user_info.birthday.year - (today.month, today.day)) < (user_info.birthday.month, user_info.birthday.day)
        
        if age < competition.min_age or age > competition.max_age:
            raise serializers.ValidationError(
                f"Возрастные ограничения: от {competition.min_age} до {competition.max_age} лет"
            )

        # 2. Проверка региональных ограничений
        if hasattr(competition, 'permissions') and isinstance(competition.permissions, list):
            if user_region not in competition.permissions:
                allowed_regions = Region.objects.filter(
                    id__in=competition.permissions
                ).values_list('name', flat=True)
                
                raise serializers.ValidationError({
                    "regional_restriction": {
                        "message": "Ваш регион не участвует в этом соревновании",
                        "user_region": user_region,
                        "allowed_regions": list(allowed_regions)
                    }
                })

        # 3. Проверка существующей заявки
        if UserApplication.objects.filter(user=user_info.id, competition=competition.id).exists():
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
        user_id = self.context['request'].user.id
        return UserApplication.objects.create(
            user=user_id,
            **validated_data
        )
        
class ApplicationDecisionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'], required=True)
    reason = serializers.CharField(required=False, allow_blank=True)
    
class UserInfoSerializer(serializers.ModelSerializer):
    nickName = serializers.CharField(source='user.nickName')  # Доступ к полю из связанной модели User
    class Meta:
        model = UserInfo
        fields = ['surname', 'name', 'nickName']