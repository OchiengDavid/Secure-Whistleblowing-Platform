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
    list_display = ('id', 'subject', 'submitted_at', 'encryption_status_label', 'unlock_link')
    readonly_fields = ('submitted_at', 'encryption_status_label')

    # 1. This adds a button to the list view
    def unlock_link(self, obj):
        if obj.attachment and 'enc_' in obj.attachment.name:
            return mark_safe(f'<a class="button" href="{obj.id}/decrypt/">🔓 Open Portal</a>')
        return "N/A"
    unlock_link.short_description = "Action"

    def encryption_status_label(self, obj):
        if obj.attachment and 'enc_' in obj.attachment.name:
            return mark_safe('<b style="color: #28a745;">🔒 SECURED</b>')
        return mark_safe('<b style="color: #dc3545;">⚠️ UNSECURED</b>')

    # 2. This creates the secret URL for the decryption box
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/decrypt/', self.admin_site.admin_view(self.decrypt_view), name='decrypt_view'),
        ]
        return custom_urls + urls

    # 3. This is the logic for the "Box"
    def decrypt_view(self, request, object_id):
        obj = self.get_object(request, object_id)
        decrypted_img = None
        error = None

        if request.method == 'POST':
            private_key_hex = request.POST.get('private_key')
            try:
                # Setup NaCl
                priv_key = nacl.public.PrivateKey(private_key_hex, nacl.encoding.HexEncoder)
                sealed_box = nacl.public.SealedBox(priv_key)
                
                # Decrypt
                encrypted_data = obj.attachment.read()
                raw_data = sealed_box.decrypt(encrypted_data)
                
                # Encode for browser display
                encoded_img = base64.b64encode(raw_data).decode('utf-8')
                decrypted_img = f"data:image/png;base64,{encoded_img}"
            except Exception:
                error = "Invalid Private Key! Access Denied."

        return render(request, 'admin/decrypt_portal.html', {
            'report': obj,
            'decrypted_img': decrypted_img,
            'error': error,
        })