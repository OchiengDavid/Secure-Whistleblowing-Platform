from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# We import the entire views module from the reports app
from reports import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Landing Page
    path('', views.landing_page, name='landing_page'),
    
    # Whistleblower Actions
    path('submit/', views.submit_report, name='submit_report'),
    path('status/', views.check_status, name='check_status'),
    
    # Admin Decryption Portal
    path('reports/<int:report_id>/decrypt/', views.decrypt_portal, name='decrypt_portal'),
]

# This allows Django to "see" the media folder where leaks are stored
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)