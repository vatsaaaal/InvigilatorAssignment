from django.db import models
from django.contrib import admin

class Room(models.Model):
    number = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return str(self.number)

    class Meta:
        ordering = ('number',)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity')

class PastList(models.Model):
    date = models.CharField(max_length=200)

    def __str__(self):
        return self.date

class SingleSubject(models.Model):
    pastList = models.ForeignKey("PastList", on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True)
    duration = models.CharField(max_length=200, blank=True)
    start_time = models.CharField(max_length=200, blank=True)
    end_time = models.CharField(max_length=200, blank=True)
    num_of_students = models.CharField(max_length=200, blank=True)
    room_num = models.CharField(max_length=200, blank=True)
    invigi_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return (str(self.pastList.date) + " - " + self.subject)