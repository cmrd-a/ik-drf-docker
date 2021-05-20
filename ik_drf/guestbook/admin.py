from django.contrib import admin
from .models import Entry, Like, ForbiddenWord

admin.site.register(Entry)
admin.site.register(Like)
admin.site.register(ForbiddenWord)
