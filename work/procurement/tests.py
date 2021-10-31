from django.test import TestCase
from projects.models import Project
from vendor.models import Vendor, VendorUnit
from rest_framework.exceptions import ValidationError

from .models import Unit, UnitConversion, Category, Item, Specification, SpecificationValue, Request


class ItemTestCase(TestCase):
    def setUp(self):
        Project.objects.create(pk=1, name='Pune Metro')
        Unit.objects.create(pk=1, name='Cement Bag', symbol='C-Bag')
        Unit.objects.create(pk=2, name='Cement Bulker Ton', symbol='C-MT')
        UnitConversion.objects.create(pk=1, primary=Unit.objects.get(pk=1), secondary=Unit.objects.get(pk=2),
                                      ratio=0.05)
        Category.objects.create(pk=1, name='Cement')
        Specification.objects.create(pk=1, name='Grade')
        SpecificationValue.objects.create(pk=1, name='OPC-43', specification=Specification.objects.get(pk=1))
        SpecificationValue.objects.create(pk=2, name='OPC-53', specification=Specification.objects.get(pk=1))
        SpecificationValue.objects.create(pk=3, name='PPC-43', specification=Specification.objects.get(pk=1))
        SpecificationValue.objects.create(pk=4, name='PPC-53', specification=Specification.objects.get(pk=1))
        Item.objects.create(pk=1,
                            name='OPC-43',
                            category=Category.objects.get(pk=1),
                            unit_of_measurement=Unit.objects.get(pk=1))
        Item.objects.get(pk=1).specification.add(SpecificationValue.objects.get(pk=1))
        Request.objects.create(pk=1,
                               project=Project.objects.get(pk=1),
                               item=Item.objects.get(pk=1),
                               date_required='2021-11-01',
                               requested_quantity=100)
        Request.objects.create(pk=2,
                               project=Project.objects.get(pk=1),
                               item=Item.objects.get(pk=1),
                               date_required='2021-11-15',
                               request_unit=Unit.objects.get(pk=2),
                               requested_quantity=10)

    def test_reverse_conversion(self):
        self.assertRaises(ValidationError, UnitConversion.objects.create, primary=Unit.objects.get(pk=2),
                          secondary=Unit.objects.get(pk=1), ratio=0.05)
        self.assertEqual(UnitConversion.objects.get(pk=1).get_inverse_ratio(), 20)

    def test_item_creation(self):
        self.assertEqual(set(Item.objects.get(pk=1).specification.all()),
                         set(SpecificationValue.objects.all().filter(pk=1)))

    def test_request_creation(self):
        self.assertEqual(Request.objects.get(pk=1).quantity, 100)
        self.assertEqual(Request.objects.get(pk=1).request_unit, Unit.objects.get(pk=1))
        self.assertEqual(Request.objects.get(pk=2).quantity, 200)
        self.assertEqual(Request.objects.get(pk=2).requested_quantity, 10)
        self.assertEqual(Request.objects.get(pk=1).state, 'Created')
        self.assertEqual(Request.objects.get(pk=2).state, 'Created')

    def test_request_rfq(self):
        pass

# Create your tests here.
