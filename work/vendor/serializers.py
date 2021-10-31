from rest_framework.serializers import ModelSerializer
from .models import Vendor, VendorUnit


class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'created', 'modified', 'vendorunit_set']
        depth = 1


class VendorUnitSerializer(ModelSerializer):
    class Meta:
        model = VendorUnit
        fields = '__all__'
