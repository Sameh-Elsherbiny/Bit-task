from django.contrib.gis.db import models


# Create your models here.


class Library(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=100)
    image = models.ImageField(upload_to='library_images', blank=True)

    def __str__(self):
        return self.name
    
class Branch(models.Model):
    address = models.CharField(max_length=100)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    location = models.PointField()
    
    def __str__(self):
        return self.library.name + ' - ' + self.address