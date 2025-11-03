from django.db import models

from django.contrib.auth.models import User

class JournalEntry(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content=models.TextField()
    image=models.ImageField(upload_to='journal_images/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.title

