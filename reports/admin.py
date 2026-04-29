import base64
import nacl.public
import nacl.encoding
from django.contrib import admin
from django.utils.html import mark_safe
from django.shortcuts import render
from django.urls import path
from .models import AnonymousReport

@admin.register(AnonymousReport)
class AnonymousReportAdmin(admin.ModelAdmin):
    # Added 'status_token' and 'status' to the list view for easy tracking
    list_display = ('id', 'status_token', 'subject', 'status', 'submitted_at', 'encryption_status_label', 'unlock_link')
    
    # We make the token and date readonly so they can't be accidentally changed
    readonly_fields = ('submitted_at', 'status_token', 'encryption_status_label')
    
    list_filter = ('status', 'submitted_at')
    search_fields = ('status_token', 'subject')

    # 'status' and 'admin_feedback' are included here so you can edit them and reply to the user
    fields = ('status_token', 'status', 'admin_feedback', 'subject', 'content', 'attachment', 'submitted_at')

    # --- ORIGINAL METHODS PRESERVED ---
    def unlock_link(self, obj):
        if obj.attachment and 'enc_' in obj.attachment.name:
            return mark_safe(f'<a class="button" href="{obj.id}/decrypt/">🔓 Open Portal</a>')
        return "N/A"
    unlock_link.short_description = "Action"

    def encryption_status_label(self, obj):
        if obj.attachment and 'enc_' in obj.attachment.name:
            return mark_safe('<b style="color: #28a745;">🔒 SECURED</b>')
        return mark_safe('<b style="color: #dc3545;">⚠️ UNSECURED</b>')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/decrypt/', self.admin_site.admin_view(self.decrypt_view), name='decrypt_view'),
        ]
        return custom_urls + urls

    def decrypt_view(self, request, object_id):
        obj = self.get_object(request, object_id)
        decrypted_img = None
        error = None

        if request.method == 'POST':
            private_key_hex = request.POST.get('private_key')
            try:
                priv_key = nacl.public.PrivateKey(private_key_hex, nacl.encoding.HexEncoder)
                sealed_box = nacl.public.SealedBox(priv_key)
                
                encrypted_data = obj.attachment.read()
                raw_data = sealed_box.decrypt(encrypted_data)
                
                encoded_img = base64.b64encode(raw_data).decode('utf-8')
                
                fname = obj.attachment.name.lower()
                if ".mp3" in fname:
                    mime = "data:audio/mpeg;base64,"
                else:
                    mime = "data:image/png;base64,"
                    
                decrypted_img = f"{mime}{encoded_img}"
            except Exception:
                error = "Invalid Private Key! Access Denied."

        return render(request, 'admin/decrypt_portal.html', {
            'report': obj,
            'decrypted_img': decrypted_img,
            'error': error,
        })