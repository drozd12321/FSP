from django.urls import path
from .views import UserRegistrationView, CustomTokenObtainPairView, CompetitionCreateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('competitions/', CompetitionCreateView.as_view(), name='create-competition'),
]