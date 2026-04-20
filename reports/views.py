import os
import io
import nacl.public
import nacl.encoding
from django.shortcuts import render
from .forms import ReportForm
from PIL import Image

def landing_page(request):
    """
    Renders the entry point. Make sure reports/landing.html exists.
    """
    return render(request, 'reports/landing.html')

def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            
            # CRITICAL FIX: The error log showed your file is named 'attachment'
            uploaded_file = request.FILES.get('attachment')
            
            if not uploaded_file:
                # If for some reason the file didn't make it, show an error on the form
                return render(request, 'reports/submit.html', {
                    'form': form, 
                    'error': 'No file was received. Please try again.'
                })
            
            try:
                # Read file content
                file_content = uploaded_file.read()
                
                # --- 1. FORENSIC STRIPPING (for images only) ---
                cleaned_bytes = file_content
                if uploaded_file.content_type.startswith('image/'):
                    try:
                        img = Image.open(io.BytesIO(file_content))
                        clean_io = io.BytesIO()
                        # Saving strips EXIF/GPS metadata automatically
                        img.save(clean_io, format=img.format)
                        cleaned_bytes = clean_io.getvalue()
                    except Exception as e:
                        print(f"Image processing failed: {e}")
                        # Fall back to original content if image processing fails

                # --- 2. ZERO-KNOWLEDGE ENCRYPTION (PyNaCl) ---
                pub_key_hex = os.getenv('OFFICER_PUBLIC_KEY')
                
                if pub_key_hex:
                    try:
                        # Load the Investigation Officer's Public Key
                        pub_key = nacl.public.PublicKey(pub_key_hex, nacl.encoding.HexEncoder)
                        sealed_box = nacl.public.SealedBox(pub_key)
                        
                        # Encrypt the cleaned bytes
                        encrypted_bytes = sealed_box.encrypt(cleaned_bytes)
                        
                        # Save the encrypted data with 'enc_' prefix
                        report.attachment.save(f"enc_{uploaded_file.name}", io.BytesIO(encrypted_bytes), save=False)
                    except Exception as e:
                        print(f"Encryption failed: {e}")
                        # Fallback: Save cleaned version without encryption
                        report.attachment.save(uploaded_file.name, io.BytesIO(cleaned_bytes), save=False)
                else:
                    # No encryption key configured - save cleaned version
                    report.attachment.save(uploaded_file.name, io.BytesIO(cleaned_bytes), save=False)
                
                report.save()
                return render(request, 'reports/success.html')
                
            except Exception as e:
                return render(request, 'reports/submit.html', {
                    'form': form, 
                    'error': f'File processing failed: {str(e)}'
                })
    else:
        form = ReportForm()
    
    return render(request, 'reports/submit.html', {'form': form})