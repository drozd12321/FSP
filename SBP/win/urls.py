from django.urls import path
from .views import RegisterView, LoginView, CompetitionCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('competitions/', CompetitionCreateView.as_view(), name='create-competition'),
]
