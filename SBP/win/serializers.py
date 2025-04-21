# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Competition, CompetitionDate, Region, Discipline
from django.db import models


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'middle_name', 'nickName', 'status', 'region', 'birth_date']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
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
    
class CompetitionSerializer(serializers.ModelSerializer):
    dates = CompetitionDateSerializer()
    regions = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        many=True,
        required=True
    )
    discipline = serializers.PrimaryKeyRelatedField(
        queryset=Discipline.objects.all()
    )

    class Meta:
        model = Competition
        fields = [
            'name',
            'regions',
            'discipline',
            'description',
            'max_participants',
            'max_participants_in_team',
            'min_age',
            'max_age',
            'competition_type',
            'type',
            'dates',
        ]

    def create(self, validated_data):
        dates_data = validated_data.pop('dates')
        regions = validated_data.pop('regions')
        
        competition = Competition.objects.create(**validated_data)
        competition.regions.set(regions)
        
        CompetitionDate.objects.create(
            competition=competition,
            **dates_data
        )
        
        return competition