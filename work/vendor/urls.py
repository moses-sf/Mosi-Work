from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, VendorUnitViewSet

router = DefaultRouter()
router.register('vendor', VendorViewSet)
router.register('vendor_unit', VendorUnitViewSet)

urlpatterns = router.urls