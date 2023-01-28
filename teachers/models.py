from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, default='abc@example.com')

    def __str__(self):
        return self.name
