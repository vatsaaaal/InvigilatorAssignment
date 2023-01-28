from django.contrib import admin
from .models import PastList, Room, RoomAdmin, SingleSubject

admin.site.register(PastList)
admin.site.register(SingleSubject)
admin.site.register(Room, RoomAdmin)