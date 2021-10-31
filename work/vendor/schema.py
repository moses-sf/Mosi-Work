from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Vendor, VendorUnit


class VendorNode(DjangoObjectType):
    class Meta:
        model = Vendor
        filter_fields = {
            'id': ['exact'],
            'name': ['iexact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class VendorUnitNode(DjangoObjectType):
    class Meta:
        model = VendorUnit
        filter_fields = {
            'id': ['exact'],
            'name': ['iexact', 'icontains', 'istartswith'],
            'vendor': ['exact']
        }
        interfaces = (relay.Node,)


class Query(ObjectType):
    vendor = relay.Node.Field(VendorNode)
    all_vendors = DjangoFilterConnectionField(VendorNode)

    vendor_unit = relay.Node.Field(VendorUnitNode)
    all_vendor_units = DjangoFilterConnectionField(VendorUnitNode)
