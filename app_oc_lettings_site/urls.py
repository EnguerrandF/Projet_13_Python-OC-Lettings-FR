from django.urls import path

from app_oc_lettings_site import views


urlpatterns = [
    path('', views.index, name='index'),
]
