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
    """
    Сериализатор для создания команд.
    
    Включает валидацию:
    1. Проверка заполненности профиля создателя
    2. Проверка лимита команд в соревновании
    3. Проверка региональных ограничений соревнования
    4. Проверка прав на создание команды
    
    Особенности:
    - Поле competition: только для командных соревнований (type='team')
    - Автоматическое назначение капитана (если не модератор)
    - Установка max_members из параметров соревнования
    
    Методы:
    - validate: комплексная проверка условий создания команды
    - create: логика создания команды с обработкой капитана
    """
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
        """
        Основная валидация данных перед созданием команды.
        
        Проверяет:
        - Наличие профиля у создателя
        - Не превышен ли лимит команд в соревновании
        - Региональные ограничения соревнования
        - Права на создание команды (для соревнований с пустыми permissions)
        """
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
        """
        Создание команды с дополнительной логикой:
        
        1. Определение капитана:
           - Для обычных пользователей - сам создатель
           - Для модераторов - должен быть указан captain_id
        
        2. Установка max_members из параметров соревнования
        
        3. Автоматическое добавление капитана в состав команды
        
        4. Обновление счетчика участников (current_members)
        """
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
    """
    Сериализатор для создания приглашений в команду.
    
    Включает комплексную валидацию:
    1. Проверка что приглашающий - капитан команды
    2. Проверка что приглашаемый не является капитаном
    3. Проверка что пользователь не состоит в команде
    4. Проверка отсутствия дублирующих приглашений
    5. Проверка что пользователь не приглашает сам себя
    
    Поля:
    - team_id: ID команды (write-only)
    - user_id: ID приглашаемого пользователя (write-only)
    """
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
        """
        Основная валидация данных перед созданием приглашения.
        
        Проверяет:
        - Приглашаемый не является капитаном команды
        - Пользователь еще не в команде
        - Нет активных дублирующих приглашений
        - Пользователь не приглашает сам себя
        """
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
        """
        Создание приглашения с автоматической установкой:
        - Статуса "Ожидает"
        - Даты создания (автоматически)
        
        Возвращает созданный объект Invitation
        """
        return Invitation.objects.create(
            **validated_data,
            status='Ожидает'
        )
        
class InvitationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения приглашений с расширенными данными.
    
    Особенности:
    - Все поля только для чтения (read_only_fields)
    - Добавляет связанные данные:
      * ID и название команды
      * Название соревнования
      * Никнейм приглашенного пользователя
    
    Поля:
    - id: ID приглашения
    - team_id: ID команды
    - team_name: Название команды
    - competition_name: Название соревнования
    - user_nickname: Никнейм пользователя (из UserInfo.nickName)
    - status: Текущий статус приглашения
    """
    team_id = serializers.IntegerField(source='team.id')
    team_name = serializers.CharField(source='team.name')
    competition_name = serializers.CharField(source='team.competition.name')
    user_nickname = serializers.CharField(source='user.user.nickName')
    
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
    """
    Сериализатор для обработки ответа на приглашение
    """
    action = serializers.ChoiceField(
        choices=['accept', 'reject'],
        write_only=True,
        required=True,
        help_text="Действие: accept (принять) или reject (отклонить)"
    )

    class Meta:
        model = Invitation
        fields = ['action', 'status']
        read_only_fields = ['id', 'team', 'user', 'status']

    def validate(self, attrs):
        """
        Проверяет что приглашение в статусе 'Ожидает'
        """
        if self.instance.status != 'Ожидает':
            raise serializers.ValidationError(
                "Можно ответить только на приглашения со статусом 'Ожидает'"
            )
        return attrs

    def update(self, instance, validated_data):
        """
        Обрабатывает действие с приглашением:
        - accept: добавляет пользователя в команду (с проверками)
        - reject: отклоняет приглашение
        """
        action = validated_data['action']
        team = instance.team
        
        if action == 'accept':
            # Проверка максимального количества участников
            if team.members.count() >= team.competition.max_participants:
                raise serializers.ValidationError(
                    f"Команда уже достигла максимума ({team.competition.max_participants} участников)"
                )
            
            # Проверка что пользователь не уже в команде
            if team.members.filter(id=instance.user.id).exists():
                raise serializers.ValidationError(
                    "Вы уже состоите в этой команде"
                )
            
            # Добавляем пользователя в команду
            team.members.add(instance.user)
            instance.status = 'Принято'
        else:
            # Отклоняем приглашение
            instance.status = 'Отклонено'
        
        instance.save()
        return instance
    
class RegionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регионов
    Возвращает только id и название региона
    """
    class Meta:
        model = Region
        fields = ['id', 'name']  # Только основные поля
        

        
class TeamApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и просмотра заявок команд.
    
    Включает:
    - Основную информацию о заявке
    - Название команды и соревнования
    - Список участников команды
    
    Валидация:
    - Проверяет, что пользователь является участником команды
    - Удаляет все приглашения для команды при создании заявки
    """
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        write_only=True
    )
    competition_name = serializers.CharField(source='competition.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    team_members = serializers.SerializerMethodField()
    status = serializers.CharField(default='pending')  # Устанавливаем значение по умолчанию
    
    class Meta:
        model = TeamApplication
        fields = ['id','team_id', 'status', 'reason', 'competition', 
                 'competition_name', 'team_name', 'team_members']
        extra_kwargs = {
            'team_id': {'required': True},
            'competition': {'write_only': True}
        }

    def get_team_members(self, obj):
        """Возвращает список участников команды"""
        members = obj.team.members.all()
        return [{
            'surname': member.surname,
            'name': member.name,
            'patronymic': member.patronymic,
            'nickName': member.user.nickName
        } for member in members]

    def validate(self, attrs):
        """Проверяет, что пользователь является участником команды"""
        team = attrs.get('team')
        if not team:
            raise serializers.ValidationError("Команда не найдена")
        
        user = self.context['request'].user
        if not team.members.filter(user=user).exists():
            raise serializers.ValidationError("Вы не являетесь участником этой команды")
        
        return attrs

    def create(self, validated_data):
        """Создает заявку с статусом 'pending' и удаляет все приглашения для команды"""
        team = validated_data['team']
        
        # Удаляем все приглашения для этой команды
        Invitation.objects.filter(team=team).delete()
        
        # Удаляем status из validated_data, если он там есть
        validated_data.pop('status', None)
        
        # Создаем заявку с явно указанным статусом
        return TeamApplication.objects.create(
            status='pending',
            reason=None,
            **validated_data
        )
        
class TeamApplicationResponseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обработки заявки команды.
    
    Валидация:
    - Проверяет, что заявка имеет статус 'pending'
    - Для действия 'reject' требует указания причины
    """
    action = serializers.ChoiceField(
        choices=['accept', 'reject'],
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
        """Обновляет статус заявки и выполняет соответствующие действия"""
        action = validated_data['action']
        
        if action == 'accept':
            # Добавляем всех участников команды в соревнование
            for member in instance.team.members.all():
                CompetitionParticipant.objects.get_or_create(
                    competition=instance.team.competition,
                    participant=member
                )
            
            instance.status = 'accepted'
            instance.reason = None
            instance.team.save()
        else:
            instance.status = 'rejected'
            instance.reason = validated_data['reason']
        
        instance.save()
        return instance
    

class DisciplineSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Discipline (Дисциплина).
    
    Используется для:
    - Сериализации данных дисциплины (преобразование в JSON)
    - Десериализации данных (проверка и преобразование JSON в модель)
    
    Поля:
    - id (int): уникальный идентификатор дисциплины (автоматически генерируется)
    - name (str): название дисциплины (обязательное поле)

    """
    class Meta:
        model = Discipline
        fields = ['id', 'name']

        
class CompetitionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Competition.
    
    Особенности:
    - Добавляет поле discipline_name (название дисциплины)
    - Добавляет human-readable поля для типов (competition_type_display, type_display)
    - Включает вычисляемое поле permissions_status:
      * 0 - нет разрешений
      * 1 - разрешения есть, но не для всех регионов (не 89)
      * 2 - полный набор разрешений (89 регионов)
    - Обрабатывает вложенный объект dates через CompetitionDateSerializer
    
    Методы:
    - create: переопределен для обработки вложенных дат
    - get_permissions_status: вычисляет статус permissions
    """
    status = serializers.CharField(default='pending')  # ← Принудительно задаём default
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

    def validate(self, data):
        # Запрещаем изменение статуса через API, если он уже pending
        instance = getattr(self, 'instance', None)
        if instance and instance.status == 'pending' and 'status' in data:
            raise serializers.ValidationError(
                {"status": "Нельзя изменить статус соревнования, ожидающего модерации"}
            )
        return data
    def get_permissions_status(self, obj):
        if not obj.permissions:  # Если permissions пустое
            return 0
        elif len(obj.permissions) != 89:  # Если длина permissions не равна 89
            return 1
        else:  # Если длина permissions равна 89
            return 2

    def create(self, validated_data):
        dates_data = validated_data.pop('dates')

        # Принудительно устанавливаем статус 'pending' при создании
        validated_data['status'] = 'pending'

        competition = Competition.objects.create(**validated_data)

        CompetitionDate.objects.create(
            competition=competition,
            **dates_data
        )

        return competition

    
    
class FAQSerializer(serializers.ModelSerializer):
    """Сериализатор FAQ (вопрос-ответ)"""
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']
        read_only_fields = ['id']


class NewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор новостей
    Поля:
    - id, title, content
    - image_url (полный URL изображения)
    - date (в формате DD.MM.YYYY)
    """
    image_url = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image_url', 'date']
        read_only_fields = fields

    def get_image_url(self, obj):
        """Возвращает полный URL изображения или None"""
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    def get_date(self, obj):
        """Форматирует дату в DD.MM.YYYY"""
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
    """
    Сериализатор для заявок пользователей на индивидуальные соревнования.
    
    Включает:
    - Основные данные заявки
    - Название соревнования (read-only)
    - Информацию о пользователе (read-only)
    
    Валидация:
    - Проверка возрастных ограничений
    - Проверка региональных ограничений
    - Проверка дублирования заявок
    - Проверка типа соревнования
    """
    competition = serializers.PrimaryKeyRelatedField(
        queryset=Competition.objects.filter(type='individual'),
        write_only=True  # Скрываем в ответе, так как есть competition_name
    )
    competition_name = serializers.CharField(source='competition.name', read_only=True)
    user_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserApplication
        fields = ['id', 'competition', 'competition_name', 'user_info', 'status', 'reason']
        read_only_fields = ['status', 'reason']  # Эти поля заполняются автоматически

    def get_user_info(self, obj):
        """Возвращает основную информацию о пользователе"""
        return {
            'surname': obj.user.surname,
            'name': obj.user.name,
            'patronymic': obj.user.patronymic,
            'nickName': obj.user.user.nickName
        }

    def validate(self, data):
        """Основная валидация заявки перед созданием"""
        competition = data['competition']
        user = self.context['request'].user
        
        # Получаем профиль пользователя
        try:
            user_info = UserInfo.objects.get(user=user)
        except UserInfo.DoesNotExist:
            raise serializers.ValidationError("Профиль пользователя не найден")

        # 1. Проверка возраста
        today = date.today()
        age = today.year - user_info.birthday.year - ((today.month, today.day) < 
                                                     (user_info.birthday.month, user_info.birthday.day))
        
        if age < competition.min_age or age > competition.max_age:
            raise serializers.ValidationError(
                f"Возрастные ограничения: от {competition.min_age} до {competition.max_age} лет"
            )

        # 2. Проверка региона (если есть ограничения)
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

        # 3. Проверка на дубликат заявки
        if UserApplication.objects.filter(user=user_info, competition=competition).exists():
            raise serializers.ValidationError(
                "Вы уже подавали заявку на это соревнование"
            )

        # 4. Проверка типа соревнования
        if competition.type != 'individual':
            raise serializers.ValidationError(
                "Заявки подаются только на индивидуальные соревнования"
            )

        return data

    def create(self, validated_data):
        """Создание заявки с привязкой к пользователю"""
        user = self.context['request'].user
        user_info = UserInfo.objects.get(user=user)
        return UserApplication.objects.create(
            user=user_info,
            **validated_data
        )
        
class ApplicationDecisionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обработки решения по заявке пользователя
    
    Поля:
    - action: accept/reject - решение организатора
    - reason: причина отказа (требуется для reject)
    - status: текущий статус заявки (read-only)
    
    Валидация:
    - Проверяет наличие причины при отклонении
    - Запрещает изменять уже обработанные заявки
    """
    action = serializers.ChoiceField(
        choices=['accept', 'reject'], 
        write_only=True,
        help_text="Действие: accept - принять, reject - отклонить"
    )
    reason = serializers.CharField(
        required=False, 
        allow_blank=True, 
        write_only=True,
        help_text="Причина отказа"
    )

    class Meta:
        model = UserApplication
        fields = ['status', 'reason', 'action']
        read_only_fields = ['status']
    
class UserInfoSerializer(serializers.ModelSerializer):
    """
    Сериализатор основной информации о пользователе
    Включает:
    - Фамилию, имя
    - Никнейм из связанной модели User
    - Рейтинг пользователя
    """
    nickName = serializers.CharField(source='user.nickName')  # Доступ к полю из связанной модели User
    class Meta:
        model = UserInfo
        fields = ['id' ,'surname', 'name', 'nickName', 'rating']
        
class VacancyResponseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для откликов на вакансии в командах
    
    Поля только для чтения:
    - Информация о команде (название)
    - Данные пользователя (ФИО, никнейм)
    - Статус отклика
    
    Поля для записи:
    - ID команды (передается как team_id)
    - Описание (передается как description, сохраняется в text)
    
    Логика:
    - При создании преобразует team_id в объект Team
    - Сохраняет description в поле text
    """
    team_name = serializers.CharField(source='team.name', read_only=True)
    user_surname = serializers.CharField(source='user.surname', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_nickname = serializers.CharField(source='user.user.nickName', read_only=True)
    
    # Поля для ввода (клиентские имена)
    team_id = serializers.IntegerField(write_only=True, source='id')  # Переименовано для ясности
    description = serializers.CharField(write_only=True)  # Будет преобразовано в text

    class Meta:
        model = VacancyResponse
        fields = [
            'id',          # будет read_only (так как это ID отклика)
            'team_id',     # write_only (из запроса)
            'description', # write_only (из запроса)
            'text',       # read_only (для ответа)
            'status', 
            'team',       # read_only (для ответа)
            'team_name', 
            'user',
            'user_surname',
            'user_name',
            'user_nickname'
        ]
        read_only_fields = ['id', 'status', 'team', 'text', 'team_name', 
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
    """
    Сериализатор для действий с откликами (принять/отклонить)
    
    Поля:
    - action: accept/reject
    - response_id: ID отклика
    """
    action = serializers.ChoiceField(choices=['accept', 'reject'])
    response_id = serializers.IntegerField()
    
class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления данных пользователя (email, nickName)"""
    class Meta:
        model = User
        fields = ['email', 'nickName']
        extra_kwargs = {
            'email': {'required': False},
            'nickName': {'required': False}
        }

class UserInfoUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления данных профиля (ФИО, регион, роль, дата рождения)"""
    class Meta:
        model = UserInfo
        fields = ['surname', 'name', 'patronymic', 'region', 'role', 'birthday',  'user_id']
        extra_kwargs = {
            'region': {'required': False},
            'role': {'required': False},
            'birthday': {'required': False}
        }

class UserProfileUpdateSerializer(serializers.Serializer):
    """
    Композитный сериализатор для обновления профиля
    
    Позволяет обновлять:
    - Данные пользователя (через user)
    - Данные профиля (через info)
    """
    user = UserUpdateSerializer(required=False)
    info = UserInfoUpdateSerializer(required=False)
    
class CompetitionShortSerializer(serializers.ModelSerializer):
    """
    Краткий сериализатор соревнований для истории участия
    
    Поля:
    - id: идентификатор соревнования
    - name: название соревнования
    - discipline: название дисциплины
    - type: тип соревнования (индивидуальное/командное)
    - status: текущий статус
    """
    discipline = serializers.CharField(source='discipline.name')
    
    class Meta:
        model = Competition
        fields = ['id', 'name', 'discipline', 'type', 'status']

class ParticipationHistorySerializer(serializers.ModelSerializer):
    """
    Сериализатор истории участия в соревнованиях
    
    Поля:
    - competition: краткая информация о соревновании
    - result: занятое место (null если соревнование еще не завершено)
    """
    competition = CompetitionShortSerializer()
    
    class Meta:
        model = CompetitionParticipant
        fields = ['competition', 'result']
        
class OrganizerCompetitionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения соревнований организатора
    
    Особенности:
    - Формирует удобную структуру данных о соревновании
    - Включает название дисциплины вместо ID
    - Убрано избыточное указание source для поля rated
    """
    competition = serializers.SerializerMethodField()
    rated = serializers.BooleanField()  # Убрано source='rated' так как оно избыточно
    
    class Meta:
        model = CompetitionOrganizer
        fields = ['competition', 'rated']
    
    def get_competition(self, obj):
        competition = obj.competition
        discipline_name = competition.discipline.name  # Оптимизировано - используем select_related
        return {
            'id': competition.id,
            'name': competition.name,
            'discipline': discipline_name,
            'type': competition.type,
            'status': competition.status
        }
        
class ResultDistributionSerializer(serializers.Serializer):
    """
    Сериализатор для данных о результате участника
    
    Поля:
    - user_id: ID участника (обязательное)
    - result: занятое место (целое число ≥ 1, обязательное)
    """
    user_id = serializers.IntegerField()
    result = serializers.IntegerField(min_value=1)

class CompetitionResultsSerializer(serializers.Serializer):
    """
    Сериализатор для запроса на распределение результатов
    
    Поля:
    - competition_id: ID соревнования (обязательное)
    - results: массив результатов участников (обязательное)
    """
    competition_id = serializers.IntegerField()
    results = ResultDistributionSerializer(many=True)
    
class MemberNicknameSerializer(serializers.ModelSerializer):
    """
    Упрощенный сериализатор для отображения ника участника
    
    Поля:
    - id: ID пользователя
    - nickName: никнейм пользователя
    """
    class Meta:
        model = User
        fields = ['id', 'nickName']

class TeamListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка команд пользователя
    
    Поля:
    - id: ID команды
    - name: название команды
    - competition_id: ID соревнования
    - competition_name: название соревнования
    - competition_status: статус соревнования
    - discipline_name: название дисциплины
    - members: список участников (ID и никнейм)
    - captain: ID капитана
    - is_register: флаг регистрации команды
    
    Особенности:
    - Использует оптимизированные методы для получения данных
    - Поддерживает аннотированное поле is_register
    """
    competition_name = serializers.CharField(source='competition.name')
    competition_status = serializers.CharField(source='competition.status')
    discipline_name = serializers.CharField(source='competition.discipline.name')
    members = serializers.SerializerMethodField()
    is_register = serializers.SerializerMethodField()
    competition_id = serializers.IntegerField(source='competition.id')  # Добавляем ID соревнования
    
    class Meta:
        model = Team
        fields = [
            'id',  # ID команды уже здесь
            'name', 
            'competition_id',  # Добавляем ID соревнования
            'competition_name', 
            'competition_status',
            'discipline_name',
            'members',
            'captain',
            'is_register',
        ]
    
    def get_members(self, obj):
        members = obj.members.all().select_related('user')
        return [{
            'id': member.user.id,
            'nickName': member.user.nickName
        } for member in members]
    
    def get_is_register(self, obj):
        # Используем аннотацию из представления, если она есть
        if hasattr(obj, 'is_register'):
            return obj.is_register
        # Иначе делаем отдельный запрос
        return TeamApplication.objects.filter(team=obj).exists()
        
    
class IndividualParticipantSerializer(serializers.ModelSerializer):
    """
    Сериализатор участников индивидуальных соревнований
    
    Поля:
    - user_id: ID пользователя
    - nickName: никнейм пользователя
    - name: имя участника
    - surname: фамилия участника
    - status: статус заявки (всегда 'approved')
    """
    user_id = serializers.IntegerField(source='user.id')
    nickName = serializers.CharField(source='user.user.nickName')
    name = serializers.CharField(source='user.name')
    surname = serializers.CharField(source='user.surname')
    
    class Meta:
        model = UserApplication
        fields = ['user_id', 'nickName', 'name', 'surname', 'status']

class TeamParticipantSerializer(serializers.ModelSerializer):
    """
    Сериализатор участников командных соревнований
    
    Поля:
    - team_id: ID команды
    - team_name: название команды
    - captain: информация о капитане
    - members: список участников команды
    - status: статус заявки (всегда 'approved')
    """
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
    """
    Сериализатор для представления данных регионального представителя
    
    Поля:
    - surname: Фамилия представителя
    - name: Имя представителя
    - patronymic: Отчество представителя
    - email: Email из связанной модели User
    - region_name: Название региона из связанной модели Region
    
    Особенности:
    - Объединяет данные из UserInfo, User и Region
    - Использует source для доступа к связанным полям
    """
    email = serializers.EmailField(source='user.email')
    region_name = serializers.CharField(source='region.name')
    
    class Meta:
        model = UserInfo
        fields = ['surname', 'name', 'patronymic', 'email', 'region_name']
        
class TeamWithCompetitionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для команды с информацией о соревновании
    
    Поля:
    - id: ID команды
    - name: Название команды
    - description: Описание команды
    - competition: Краткая информация о соревновании (использует CompetitionShortSerializer)
    
    Особенности:
    - Включает вложенную информацию о соревновании
    - Используется для отображения команд с контекстом их участия
    """
    competition = CompetitionShortSerializer()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'competition']

class UserVacancyResponseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для откликов пользователя на вакансии в командах
    
    Поля:
    - id: ID отклика
    - text: Текст отклика
    - status: Статус отклика (код)
    - status_display: Человекочитаемое название статуса
    - team: Информация о команде с соревнованием
    
    Особенности:
    - Включает человекочитаемое отображение статуса через get_status_display()
    - Предоставляет полную информацию о команде и связанном соревновании
    - Используется для отображения истории откликов пользователя
    """
    team = TeamWithCompetitionSerializer()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = VacancyResponse
        fields = ['id', 'text', 'status', 'status_display', 'team']
        
class CompetitionDecisionSerializer(serializers.Serializer):
    competition_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['accept', 'reject'])