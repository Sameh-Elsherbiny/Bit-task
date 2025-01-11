from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Library(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=100)
    email = models.EmailField(_("Email"), max_length=100)
    website = models.URLField(_("Website"), max_length=100)
    image = models.ImageField(_("Image"), upload_to='library_images', blank=True)

    def __str__(self):
        return self.name
    
class Branch(models.Model):
    address = models.CharField(_("Address"), max_length=100)
    library = models.ForeignKey(Library, verbose_name=_("Library"), on_delete=models.CASCADE)
    location = models.PointField(_("Location"))
    
    def __str__(self):
        return self.library.name + ' - ' + self.address
    
