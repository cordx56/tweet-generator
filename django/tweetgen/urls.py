from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('api/v1/tweetgen/authRedirect/', views.AuthRedirectAPIView.as_view()),
    path('api/v1/tweetgen/authAndGen/', views.AuthAndGenAPIView.as_view()),
    path('api/v1/tweetgen/authAndDel/', views.AuthAndDelAPIView.as_view()),

    path('api/v1/tweetgen/genText/', views.GenTextAPIView.as_view()),
    path('api/v1/tweetgen/genText/<screen_names>', views.GenTextAPIView.as_view()),

    # Twitter card image
    path('api/v1/tweetgen/genImage/', views.GenImageAPIView.as_view()),
    path('api/v1/tweetgen/genImage/<screen_name>', views.GenImageAPIView.as_view()),
]
