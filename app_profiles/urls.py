from django.urls import path

from app_profiles import views

urlpatterns = [
    path('profiles/', views.profiles_index, name='profiles_index'),
    path('profiles/<str:username>/', views.profile, name='profile'),
]
