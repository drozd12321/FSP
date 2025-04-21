# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

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
    STATUS_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('other', 'Другое'),
    )

    email = models.EmailField(unique=True, null=True, blank=True)
    nickName = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    region = models.CharField(max_length=100)
    birth_date = models.DateField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'nickName'  # Для логина по умолчанию
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'status', 'region', 'birth_date']

    def __str__(self):
        return self.nickName
