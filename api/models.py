from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Image(models.Model):
    caption = models.CharField(max_length=255)
    caption_color = models.JSONField()  # {r: 255, g: 255, b: 255}
    caption_position = models.JSONField()  # {x: , y: }
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.FileField(upload_to='images/')

    def __str__(self):
        return self.caption


class Album(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Relationship(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followed')
