from django.contrib import admin
from .models import Album, Image, Tag, Relationship

# Register your models here.
admin.site.register(Album)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Relationship)
