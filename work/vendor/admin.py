from django.contrib import admin
from .models import Vendor, VendorUnit


# Register your models here.
admin.site.register(Vendor)
admin.site.register(VendorUnit)