from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/ranking/', views.RankingGenerateAPIView.as_view()),
]
