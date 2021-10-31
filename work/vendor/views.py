from rest_framework.viewsets import ModelViewSet
from .models import Vendor, VendorUnit

from .serializers import VendorSerializer, VendorUnitSerializer


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorUnitViewSet(ModelViewSet):
    queryset = VendorUnit.objects.all()
    serializer_class = VendorUnitSerializer
