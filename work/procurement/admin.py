from django.contrib import admin
from .models import *


admin.site.register(Unit)
admin.site.register(UnitConversion)
admin.site.register(Specification)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(SpecificationValue)
admin.site.register(Request)