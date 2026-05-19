from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Google OAuth
    path('auth/', include('social_django.urls', namespace='social')),

    # REST API
    path('api/auth/',      include('users.urls')),
    path('api/operators/', include('operators.urls')),
    path('api/routes/',    include('routes.urls')),

    # Auto-generated API docs at /api/docs/
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/',   SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
