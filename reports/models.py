from django.db import models
import nacl.exceptions

class AnonymousReport(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    attachment = models.FileField(upload_to='leaks/')
    submitted_at = models.DateTimeField(auto_now_add=True) # Check this name!
    def __str__(self):
        return self.subject
