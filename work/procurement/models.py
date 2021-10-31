import kwargs as kwargs
import specification as specification
from django.db import models
from django.db.models import ManyToManyField
from django_extensions.db.models import TimeStampedModel
from rest_framework.exceptions import ValidationError


class Unit(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.symbol


class UnitConversion(TimeStampedModel):
    primary = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='primary')
    secondary = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='secondary')
    ratio = models.FloatField()

    def clean(self):
        same = UnitConversion.objects.all().filter(primary=self.primary, secondary=self.secondary)
        reverse = UnitConversion.objects.all().filter(secondary=self.primary, primary=self.secondary)
        
        if same or reverse:
            raise ValidationError('Conversion already exists')

    def save(self, *args, **kwargs):
        self.clean()
        super(UnitConversion, self).save(**kwargs)

    def get_inverse_ratio(self):
        return 1/self.ratio

    def __str__(self) -> str:
        return f'{self.primary}->{self.secondary}'


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    allowable = models.ManyToManyField('Unit', related_name='allowed_units')

    def __str__(self) -> str:
        return self.name


class Specification(TimeStampedModel):
    name = models.CharField(max_length=255)
    allowed = models.ManyToManyField('Category', related_name='allowable_category')

    def __str__(self) -> str:
        return self.name


class SpecificationValue(TimeStampedModel):
    name = models.CharField(max_length=255)
    specification = models.ForeignKey('Specification', on_delete=models.CASCADE, related_name='values')

    def __str__(self) -> str:
        return self.name


class Item(TimeStampedModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='items')
    specification = models.ManyToManyField('SpecificationValue')
    unit_of_measurement = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='uom')

    def __str__(self) -> str:
        return self.name

    def save(self, * args, **kwargs):
        super(Item, self).save(**kwargs)
        # self.unit_of_measurement.save()


class Request(TimeStampedModel):
    class StateChoices(models.TextChoices):
        created = "Created"
        rejected = "Rejected"
        rfq = "RFQ"
        ordered = "Ordered"

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.FloatField(blank=True, null=True)
    request_unit = models.ForeignKey('Unit', on_delete=models.CASCADE, blank=True, null=True)
    date_required = models.DateField()
    requested_quantity = models.FloatField()
    state = models.CharField(max_length=255, choices=StateChoices.choices, default=StateChoices.created)

    def clean(self):
        def get_ratio(initial: Unit, final: Unit) -> float:
            if UnitConversion.objects.all().filter(primary=initial, secondary=final):
                conversion = UnitConversion.objects.get(primary=initial, secondary=final)
                return conversion.ratios
            elif UnitConversion.objects.all().filter(primary=final, secondary=initial):
                conversion = UnitConversion.objects.get(primary=final, secondary=initial)
                return conversion.get_inverse_ratio()
            else:
                raise ValidationError('This conversion does not exist')

        if not self.request_unit:
            self.request_unit = self.item.unit_of_measurement
        if self.request_unit != self.item.unit_of_measurement:
            self.quantity = round(self.requested_quantity * get_ratio(self.request_unit, self.item.unit_of_measurement),
                                  2)
        else:
            self.quantity = self.requested_quantity

    def save(self, *args, **kwargs):
        self.clean()
        super(Request, self).save(**kwargs)

    def __str__(self):
        return f'{self.project}-{self.item}-{self.created}'


class VendorRFQ(TimeStampedModel):
    class StateChoices(models.TextChoices):
        initiated = "initiated"
        clarifications = "clarifications"
        response_received = "response_received"
        not_applicable = "not_applicable"
        open = "open"
        closed = "closed"

    vendor = models.ForeignKey('vendor.VendorUnit', on_delete=models.CASCADE)
    state = models.CharField(max_length=50, choices=StateChoices.choices, blank=True)

    def set_state(self, state):
        self.state = state
        self.save()

    def clean(self):
        if not self.state:
            self.set_state('initiated')

    def save(self, *args, **kwargs):
        self.clean()
        super(VendorRFQ, self).save(**kwargs)


class VendorRFQItem(TimeStampedModel):
    class ApprovalStatus(models.TextChoices):
        approved = 'approved'
        open = 'open'
        rejected = 'rejected'

    vendor_rfq = models.ForeignKey('VendorRFQ', on_delete=models.CASCADE)
    request = models.ForeignKey('Request', on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=30, choices=ApprovalStatus.choices)
    rate = models.FloatField(blank=True, null=True)


class VendorPO(TimeStampedModel):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    vendor_item = models.ForeignKey('vendor.VendorUnit', on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='procurement/po/')


class VendorPOItem(TimeStampedModel):
    po = models.ForeignKey('VendorPO', on_delete=models.CASCADE)
    rfq_item = models.ForeignKey('VendorRFQItem', on_delete=models.CASCADE)


class VendorRFQAction(TimeStampedModel):
    class Actions(models.TextChoices):
        email_sent = 'email_sent'
        email_received = 'email_received'
        comment = 'comment'
        discussion = 'discussion'

    vendor_rfq = models.ForeignKey('VendorRFQ', on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100, choices=Actions.choices)
    details = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='vendor/rfqAction/')
