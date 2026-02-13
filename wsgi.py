from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', RedirectView.as_view(url='/admin-dashboard/', permanent=False)),
    
    # API endpoints
    path('api/users/', include('apps.users.urls')),
    
    # UI endpoints
    path('', include('apps.ui.urls')),
    path('auth/', include('apps.users.urls')),
    path('content/', include('apps.content.urls')),
    path('assessments/', include('apps.assessments.urls')),
    path('analytics/', include('apps.analytics.urls')),
]
