from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='author_images', blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images', blank=True)

    def __str__(self):
        return self.title
