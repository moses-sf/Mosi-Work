from django.db import models
from django_extensions.db.models import TimeStampedModel


# Create your models here.
class Vendor(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class VendorUnit(TimeStampedModel):
    name = models.CharField(max_length=255)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.vendor}-{self.name}'
