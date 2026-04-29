import os
import io
import base64
import nacl.public
import nacl.encoding
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReportForm
from .models import AnonymousReport 
from PIL import Image
from django.conf import settings
from mutagen.mp3 import MP3

def landing_page(request):
    return render(request, 'reports/landing.html')

def check_status(request):
    report = None
    error = None
    if request.method == 'POST':
        token = request.POST.get('token', '').strip().upper()
        try:
            report = AnonymousReport.objects.get(status_token=token)
        except AnonymousReport.DoesNotExist:
            error = "Invalid Token. Please verify and try again."
            
    return render(request, 'reports/check_status.html', {'report': report, 'error': error})

def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            uploaded_file = request.FILES.get('attachment')
            
            if not uploaded_file:
                return render(request, 'reports/submit.html', {'form': form, 'error': 'No file received.'})
            
            try:
                file_content = uploaded_file.read()
                cleaned_bytes = file_content
                
                # --- 1. METADATA STRIPPING ---
                if uploaded_file.content_type.startswith('image/'):
                    img = Image.open(io.BytesIO(file_content))
                    clean_io = io.BytesIO()
                    img.save(clean_io, format=img.format) 
                    cleaned_bytes = clean_io.getvalue()
                
                elif ".mp3" in uploaded_file.name.lower():
                    temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_strip.mp3')
                    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                    
                    with open(temp_path, 'wb+') as f:
                        f.write(file_content)
                    
                    try:
                        audio = MP3(temp_path)
                        audio.delete() 
                        audio.save()
                        with open(temp_path, 'rb') as f:
                            cleaned_bytes = f.read()
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

                # --- 2. ENCRYPTION ---
                key_path = os.path.join(settings.BASE_DIR, 'public_key.key')
                with open(key_path, "rb") as f:
                    pub_key_data = f.read()
                
                public_key = nacl.public.PublicKey(pub_key_data)
                sealed_box = nacl.public.SealedBox(public_key)
                encrypted_bytes = sealed_box.encrypt(cleaned_bytes)
                
                # Save the encrypted file
                new_filename = f"enc_{uploaded_file.name}"
                report.attachment.save(new_filename, io.BytesIO(encrypted_bytes), save=False)
                
                # --- 3. SAVE & TOKEN GENERATION ---
                report.save() 
                
                # Pass the generated token to the success page
                return render(request, 'reports/success.html', {'token': report.status_token})
                
            except Exception as e:
                print(f"DEBUG ERROR: {e}")
                return render(request, 'reports/submit.html', {'form': form, 'error': str(e)})
    else:
        form = ReportForm()
    return render(request, 'reports/submit.html', {'form': form})

def decrypt_portal(request, report_id):
    report = get_object_or_404(AnonymousReport, id=report_id)
    error = None
    decrypted_img = None

    if request.method == 'POST':
        priv_key_hex = request.POST.get('private_key')
        try:
            private_key = nacl.public.PrivateKey(priv_key_hex, encoder=nacl.encoding.HexEncoder)
            sealed_box = nacl.public.SealedBox(private_key)
            
            encrypted_data = report.attachment.read()
            decrypted_data = sealed_box.decrypt(encrypted_data)
            
            base64_encoded = base64.b64encode(decrypted_data).decode('utf-8')
            fname = report.attachment.name.lower()
            
            if ".mp3" in fname:
                mime = "data:audio/mpeg;base64,"
            else:
                mime = "data:image/png;base64,"

            decrypted_img = f"{mime}{base64_encoded}"
            
        except Exception as e:
            error = "Decryption failed. Please verify your Private Key."

    return render(request, 'reports/decrypt_portal.html', {
        'report': report,
        'decrypted_img': decrypted_img,
        'error': error
    })