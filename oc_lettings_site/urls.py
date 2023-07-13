from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('app_lettings.urls')),
    path('', include('app_profiles.urls')),
    path('', include('app_oc_lettings_site.urls')),
    path('admin/', admin.site.urls),
]
