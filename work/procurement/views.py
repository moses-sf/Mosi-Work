from django.db.models import Model
from rest_framework.viewsets import ModelViewSet

from .serializers import UnitSerializer, UnitConversionSerializer, CategorySerializer, SpecificationSerializer, \
    SpecificationValueSerializer, ItemSerializer, AllItemSerializer, RequestSerializer, AllRequestSerializer, \
    AllCategorySerializer
from .models import Unit, UnitConversion, Category, Specification, SpecificationValue, Item, Request


# Create your views here.
class UnitViewSet(ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class UnitConversionViewSet(ModelViewSet):
    queryset = UnitConversion.objects.all()
    serializer_class = UnitConversionSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AllCategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = AllCategorySerializer


class SpecificationViewSet(ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer


class SpecificationValueViewSet(ModelViewSet):
    queryset = SpecificationValue.objects.all()
    serializer_class = SpecificationValueSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class AllItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = AllItemSerializer


class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class AllRequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = AllRequestSerializer
