from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from reports.views import landing_page, submit_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('submit/', submit_report, name='submit_report'),
]

# This allows Django to "see" the media folder where leaks are stored
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
