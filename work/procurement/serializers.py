from unicodedata import category

from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, ListSerializer
from rest_framework.validators import UniqueTogetherValidator

from .models import Unit, UnitConversion, Category, Specification, SpecificationValue, Item, Request, VendorRFQ, \
    VendorRFQItem, VendorPOItem, VendorPO, VendorRFQAction


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name', 'symbol', 'primary', 'secondary']
        depth = 1


class UnitConversionSerializer(ModelSerializer):
    class Meta:
        model = UnitConversion
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'items', 'allowable', 'allowable_category']


class AllCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 1


class SpecificationValueSerializer(ModelSerializer):
    class Meta:
        model = SpecificationValue
        fields = '__all__'


class SpecificationSerializer(ModelSerializer):

    class Meta:
        model = Specification
        fields = ['id', 'name', 'allowed', 'values']


class VendorRFQSerializer(ModelSerializer):
    class Meta:
        model = VendorRFQ
        fields = '__all__'


class VendorRFQItemSerializer(ModelSerializer):
    class Meta:
        model = VendorRFQItem
        fields = '__all__'


class ItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'category', 'specification', 'unit_of_measurement']
        extra_kwargs = {'specification': {'required': False, 'allow_empty': True}}
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=['name', 'category']
            ),
        ]
        # depth = 1

    def validate(self, data):
        print(data)
        if data['unit_of_measurement'] not in data['category'].allowable.all():
            raise ValidationError('Unit not valid for this Category')
        return data

    def validate_specification(self, value):
        spec_list = []
        for spec in value:
            spec_list.append(spec.specification)
        if len(set(spec_list)) != len(spec_list):
            raise ValidationError('Only one value per specification is allowed.')
        return value


class AllItemSerializer(ItemSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        depth = 1


class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

    def validate(self, data):
        print(data)
        if data['request_unit'] not in data['item'].category.allowable.all():
            raise ValidationError('Request Unit not valid for this Category')
        return data


class AllRequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
        depth = 1


class VendorPOSerializer(ModelSerializer):
    class Meta:
        model = VendorPO
        fields = '__all__'


class VendorPOItemSerializer(ModelSerializer):
    class Meta:
        model = VendorPOItem
        fields = '__all__'


class VendorRFQActionSerializer(ModelSerializer):
    class Meta:
        model = VendorRFQAction
        fields = '__all__'
