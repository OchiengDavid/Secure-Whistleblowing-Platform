from django.db import models
import nacl.exceptions
import uuid # Added for token generation

class AnonymousReport(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    attachment = models.FileField(upload_to='leaks/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # --- New Fields for Status Tracking ---
    # add null=True and blank=True temporarily
    status_token = models.CharField(max_length=12, unique=True, editable=False, null=True, blank=True)
    status = models.CharField(max_length=50, default="Pending") 
    admin_feedback = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.status_token:
            # Generates a unique 8-character code (e.g., A1B2C3D4)
            self.status_token = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} ({self.status_token})"