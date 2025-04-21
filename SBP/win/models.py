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

    def __str__(self):
        return f"{self.email} ({self.nickname})"