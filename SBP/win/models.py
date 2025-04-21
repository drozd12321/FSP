from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STATUS_CHOICES = [
        ('fsp', 'Представитель ФСП'),
        ('fspReg', 'Региональный представитель ФСП'),
        ('user', 'Участник'),
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    nickname = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    region = models.CharField(max_length=100)
    birth_date = models.DateField()
    
    username = None  # Убираем стандартное поле username
    
    USERNAME_FIELD = 'email'  # Аутентификация по email
    REQUIRED_FIELDS = ['first_name', 'last_name', 'nickname', 'status', 'region', 'birth_date']



class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    

class UserInfo(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='users')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
    birthday = models.DateField()
    nickname = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.surname} {self.name} ({self.nickname})"

class UserStats(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, primary_key=True)
    competitions_count = models.PositiveIntegerField(default=0)
    points_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.user.nickname}: {self.competitions_count} competitions, {self.points_count} points"

class Discipline(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Competition(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'
    COMPETITION_TYPE_CHOICES = [
        (ONLINE, 'Online'),
        (OFFLINE, 'Offline'),
    ]

    INDIVIDUAL = 'individual'
    TEAM = 'team'
    TYPE_CHOICES = [
        (INDIVIDUAL, 'Individual'),
        (TEAM, 'Team'),
    ]

    max_participants = models.IntegerField()
    name = models.CharField(max_length=50)
    competition_type = models.CharField(max_length=10, choices=COMPETITION_TYPE_CHOICES)
    status = models.CharField(max_length=25)
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
   
class CompetitionHistory(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='competition_histories')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='competition_histories')

class Team(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(UserInfo, related_name='teams')
    captain = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True, related_name='captain_teams')

    def __str__(self):
        return f"{self.name} ({self.competition})"

class Invitation(models.Model):

    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='invitations')
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(max_length=25)

    def __str__(self):
        return f"Invitation of {self.user} to {self.team} - {self.status}"
    
class TeamApplication(models.Model):

    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=25)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Team Application"
        verbose_name_plural = "Team Applications"

    def __str__(self):
        return f"Application from {self.team.name} - {self.status}"

class UserApplication(models.Model):

    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=25)
    reason = models.TextField(blank=True, null=True)  # причина отказа или комментарий

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Application"
        verbose_name_plural = "User Applications"

    def __str__(self):
        return f"Application from {self.user.nickname} - {self.status}"

class TeamRole(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Vacancy(models.Model):

    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='vacancies')
    role = models.ForeignKey(TeamRole, on_delete=models.PROTECT, related_name='vacancies')
    status = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vacancy '{self.role}' in {self.team.name} - {self.status}"
    
class VacancyResponse(models.Model):

    text = models.TextField()
    status = models.CharField(max_length=25)
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='responses')

    def __str__(self):
        return f"Response by {self.user.nickname} to {self.vacancy.role.name} - {self.status}"
    
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
    
class CompetitionOrganizer(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='organized_competitions')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='organizers')

    class Meta:
        unique_together = ('user', 'competition')  # чтобы один пользователь не был организатором одного соревнования несколько раз

    def __str__(self):
        return f"Organizer {self.user} for {self.competition}"