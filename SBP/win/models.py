
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.validators import MinValueValidator

class UserManager(BaseUserManager):
    def create_user(self, email, nickName, password=None, **extra_fields):
        if not email and not nickName:
            raise ValueError('Email или NickName должны быть указаны')
        email = self.normalize_email(email)
        user = self.model(email=email, nickName=nickName, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickName, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True.')
        return self.create_user(email, nickName, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    nickName = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'nickName'  # Для логина по умолчанию
    REQUIRED_FIELDS = ['email']


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='users')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
    birthday = models.DateField(null=True)
    tg_username = models.CharField(max_length=30, null=True, blank=True)


    is_approved = models.BooleanField(default=False)  # Новое поле
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")  # Добавляем это
    
    def update_rating(self):
        """Метод для обновления рейтинга"""
        from .utils import calculate_user_rating
        self.rating = calculate_user_rating(self)
        self.save(update_fields=['rating'])
    def __str__(self):
        return f"{self.surname} {self.name} ({self.user.nickName})"

class Discipline(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class UserDisciplineStats(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='discipline_stats')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    competitions_count = models.PositiveIntegerField(default=0)
    points_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'discipline')
        verbose_name_plural = 'User discipline statistics'
    
    def __str__(self):
        return f"{self.user} in {self.discipline}: {self.competitions_count} comps, {self.points_count} pts"


class Competition(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'
    COMPETITION_TYPE_CHOICES = [
        (ONLINE, 'Онлайн'),
        (OFFLINE, 'Оффлайн'),
    ]

    INDIVIDUAL = 'individual'
    TEAM = 'team'
    TYPE_CHOICES = [
        (INDIVIDUAL, 'Личное'),
        (TEAM, 'Командное'),
    ]

    max_participants = models.IntegerField()
    max_participants_in_team = models.IntegerField()
    min_age = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    max_age = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    competition_type = models.CharField(max_length=10, choices=COMPETITION_TYPE_CHOICES)
    status = models.CharField(max_length=25, default='pending')
    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT, related_name='competitions')
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    permissions = models.JSONField(default=list, blank=True)


class CompetitionDate(models.Model):
    competition = models.OneToOneField(Competition, on_delete=models.CASCADE, related_name='dates')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()

    def __str__(self):
        return f"Dates for {self.competition}"
   
class Team(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(UserInfo, related_name='teams')
    captain = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, related_name='captain_teams')
    is_private = models.BooleanField(default=False)
    max_members = models.PositiveIntegerField()
    current_members = models.PositiveIntegerField(default=1)  # Текущее количество участников (по умолчанию 1 - капитан)

    def __str__(self):
        return f"{self.name} ({self.competition})"

    def save(self, *args, **kwargs):
        # Автоматическое обновление current_members при сохранении
        if self.pk:  # Если объект уже сохранен в БД
            self.current_members = self.members.count()
        super().save(*args, **kwargs)

    
class Invitation(models.Model):
    STATUS_CHOICES = [
        ('Ожидает', 'Ожидает'),
        ('Принято', 'Принято'),
        ('Отклонено', 'Отклонено')
    ]
    
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='invitations')
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Ожидает')

    
class TeamApplication(models.Model):

    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_applications')
    status = models.CharField(max_length=25)
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='team_applications')
    reason = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Team Application"
        verbose_name_plural = "Team Applications"

    def __str__(self):
        return f"Application from {self.team.name} - {self.status}"

class UserApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    ]
    
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='user_applications')
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='user_applications')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['user', 'competition']  # Одна заявка от пользователя на соревнование
        verbose_name = "User Application"
        verbose_name_plural = "User Applications"

    def __str__(self):
        return f"Application from {self.user} to {self.competition} - {self.status}"
       
class VacancyResponse(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (PENDING, 'В рассмотрении'),
        (ACCEPTED, 'Принято'),
        (REJECTED, 'Отклонено'),
    ]

    text = models.TextField()
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(
        UserInfo,  # Или 'UserInfo' если используете эту модель
        on_delete=models.CASCADE,
        related_name='responses'
    )

    def __str__(self):
        return f"Отклик от {self.user} в команду {self.team.name}"
    
class PrizePoints(models.Model):

    competition_type = models.CharField(max_length=20)
    place = models.PositiveIntegerField()
    points = models.PositiveIntegerField()

    class Meta:
        ordering = ['competition_type', 'place']
        verbose_name = 'Призовые баллы'
        verbose_name_plural = 'Призовые баллы'

    def __str__(self):
        return f"{self.competition_type} - Место {self.place}: {self.points} баллов"
    
class CompetitionParticipant(models.Model):
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='participants')
    participant = models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='competition_participations')
    result = models.PositiveIntegerField(validators=[MinValueValidator(1)], null = True, default=0)
    
class CompetitionOrganizer(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='organized_competitions')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='organizers')
    rated = models.BooleanField()
    class Meta:
        unique_together = ('user', 'competition')  # чтобы один пользователь не был организатором одного соревнования несколько раз

    def __str__(self):
        return f"Organizer {self.user} for {self.competition}"

class CompetitionResult(models.Model):
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='results')
    participant = models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='competition_results')
    place = models.PositiveIntegerField()

    class Meta:
        unique_together = ('competition', 'participant')  # один результат на участника в соревновании
        ordering = ['place']  # сортировка по месту

    def __str__(self):
        return f"{self.participant} - {self.place} место в {self.competition}"
    
class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"

    def __str__(self):
        return self.question[:50] + "..." if len(self.question) > 50 else self.question
    
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(
        upload_to='news/',
        null=True,
        blank=True,
        verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title