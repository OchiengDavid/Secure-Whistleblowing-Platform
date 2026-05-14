import base64
from django.urls import path
from django.utils.decorators import method_decorator
from django_otp.decorators import otp_required
from django.contrib import admin
from django.utils.html import mark_safe
from django.shortcuts import render
import nacl.public
import nacl.encoding
from .models import AnonymousReport


@admin.register(AnonymousReport)
class AnonymousReportAdmin(admin.ModelAdmin):

    list_display = ('status_token', 'subject', 'status', 'submitted_at', 'encryption_status_label', 'unlock_link')
    readonly_fields = ('submitted_at', 'status_token', 'encryption_status_label')
    list_filter = ('status', 'submitted_at')
    search_fields = ('status_token', 'subject')
    fields = ('status_token', 'status', 'admin_feedback', 'subject', 'content', 'attachment', 'submitted_at')

    # ── URL ROUTING (once only) ───────────────────────────────
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.investigator_dashboard), name='investigator_dashboard'),
            path('<path:object_id>/decrypt/', self.admin_site.admin_view(self.decrypt_view), name='decrypt_view'),
        ]
        return custom_urls + urls

    # ── VIEWS (once only each) ────────────────────────────────
    @method_decorator(otp_required)
    def investigator_dashboard(self, request):
        reports = AnonymousReport.objects.all().order_by('-submitted_at')
        return render(request, 'admin/investigator_dashboard.html', {
            'reports': reports,
            'title': 'Investigator Dashboard',
        })

    @method_decorator(otp_required)
    def decrypt_view(self, request, object_id):
        obj = self.get_object(request, object_id)
        decrypted_content = None
        decrypted_text = None
        error = None

        if request.method == 'POST':
            private_key_hex = request.POST.get('private_key', '').strip()
            try:
                priv_key = nacl.public.PrivateKey(private_key_hex, nacl.encoding.HexEncoder)
                sealed_box = nacl.public.SealedBox(priv_key)

                # Decrypt attachment
                if obj.attachment:
                    obj.attachment.seek(0)
                    encrypted_data = obj.attachment.read()
                    raw_data = sealed_box.decrypt(encrypted_data)
                    fname = obj.attachment.name.lower()
                    if '.mp3' in fname or '.wav' in fname:
                        mime = 'data:audio/mpeg;base64,'
                    elif '.pdf' in fname:
                        mime = 'data:application/pdf;base64,'
                    elif '.png' in fname:
                        mime = 'data:image/png;base64,'
                    elif '.jpg' in fname or '.jpeg' in fname:
                        mime = 'data:image/jpeg;base64,'
                    else:
                        mime = 'data:application/octet-stream;base64,'
                    encoded = base64.b64encode(raw_data).decode('utf-8')
                    decrypted_content = f'{mime}{encoded}'

                # Decrypt text content if encrypted
                if obj.content and obj.content.startswith('enc:'):
                    raw_text = sealed_box.decrypt(bytes.fromhex(obj.content[4:]))
                    decrypted_text = raw_text.decode('utf-8')
                else:
                    decrypted_text = obj.content

            except Exception:
                error = "Decryption failed — wrong private key or corrupted data."

        return render(request, 'admin/decrypt_portal.html', {
            'report': obj,
            'decrypted_content': decrypted_content,
            'decrypted_text': decrypted_text,
            'error': error,
            'title': 'Secure Decryption Portal',
        })

    # ── UI HELPERS ────────────────────────────────────────────
    def unlock_link(self, obj):
        return mark_safe(
            f'<a class="button" style="background:#007bff;color:white;padding:4px 10px;'
            f'border-radius:4px;text-decoration:none;" href="{obj.id}/decrypt/">🔓 Open Portal</a>'
        )
    unlock_link.short_description = 'Action'

    def encryption_status_label(self, obj):
        if obj.attachment and 'enc_' in obj.attachment.name:
            return mark_safe('<b style="color:#28a745;">🔒 SECURED</b>')
        return mark_safe('<b style="color:#dc3545;">⚠️ UNSECURED</b>')
    encryption_status_label.short_description = 'Encryption'