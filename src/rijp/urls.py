from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rijp_portal import views as rijp_views

CACHE_TIME_SHORT = int(getattr(settings, "CACHE_TIME_SHORT", 0))
CACHE_TIME_MEDIUM = int(getattr(settings, "CACHE_TIME_MEDIUM", 0))
CACHE_TIME_LONG = int(getattr(settings, "CACHE_TIME_LONG", 0))
SB_URL_BASE = getattr(settings, "URL_BASE", "")

urlpatterns = [
    path('', rijp_views.IndexListView.as_view(), name='index'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add custom handlers for the HTTP error codes
# handler404 = 'book.views.custom_404'
# handler500 = 'book.views.custom_500'