from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerUIView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerUIView.as_view(url_name='schema'), name='swagger-ui'),

    # App routes
    path('api/auth/',            include('apps.users.urls')),
    path('api/stations/',        include('apps.stations.urls')),
    path('api/bookings/',        include('apps.bookings.urls')),
    path('api/mobile-services/', include('apps.mobile_services.urls')),
    path('api/roadside/',        include('apps.roadside.urls')),
    path('api/loyalty/',         include('apps.loyalty.urls')),
    path('api/reminders/',       include('apps.reminders.urls')),
    path('api/payments/',        include('apps.payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
