from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from reports import views
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    # ── 1. The Admin/Developer Portal ────────────────────────
    path('admin/', admin.site.urls),

    # ── 2. The MFA Authentication Gate ───────────────────────
    # We move this to 'auth/' so it doesn't fight with the landing page
    path('auth/', include(tf_urls)),

    # ── 3. Public whistleblower pages ────────────────────────
    # These remain at the root for easy public access
    path('', views.landing_page, name='landing_page'),
    path('submit/', views.submit_report, name='submit_report'),
    path('status/', views.check_status, name='check_status'),

    # ── 4. Officer portal ────────────────────────────────────
    # Protected by @otp_required in your views.py
    path('officer/login/', views.officer_login, name='officer_login'),
    path('officer/dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('officer/decrypt/<int:report_id>/', views.officer_decrypt, name='officer_decrypt'),
    path('officer/logout/', views.officer_logout, name='officer_logout'),
]

# Handle media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)