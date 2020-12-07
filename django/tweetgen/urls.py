from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('api/v1/tweetgen/authRedirect/', views.AuthRedirectAPIView.as_view()),
    path('api/v1/tweetgen/authAndGen/', views.AuthAndGenAPIView.as_view()),
    path('api/v1/tweetgen/authAndDel/', views.AuthAndDelAPIView.as_view()),

    path('api/v1/tweetgen/genText/<screen_name>', views.GenTextAPIView.as_view()),
]
