from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Competition, CompetitionDate, Region, Discipline
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]  # Встроенная валидация пароля Django
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'password',
            'first_name', 'last_name', 'middle_name',
            'nickname', 'status', 'region', 'birth_date'
        ]

    def create(self, validated_data):
        # Пароль хранится в виде хэша (не в чистом виде!)
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Аутентификация по email или nickname
        login = attrs.get('username')
        
        if '@' in login:
            attrs['email'] = login
        else:
            attrs['nickname'] = login
            
        del attrs['username']
        
        self.user = User.objects.filter(
            models.Q(email=attrs.get('email', '')) | 
            models.Q(nickname=attrs.get('nickname', ''))
        ).first()
        
        if not self.user or not self.user.check_password(attrs['password']):
            raise serializers.ValidationError("Неверные учетные данные")
        
        data = {}
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
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