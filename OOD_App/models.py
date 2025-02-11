from django.db import models


class ContactMessage(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.user_name
