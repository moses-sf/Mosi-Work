from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UnitViewSet, UnitConversionViewSet, CategoryViewSet, SpecificationViewSet, SpecificationValueViewSet, \
    ItemViewSet, AllItemViewSet, RequestViewSet, AllRequestViewSet, AllCategoryViewSet

router = DefaultRouter()
router.register('unit', UnitViewSet)
router.register('unit_conversion', UnitConversionViewSet)
router.register('category', CategoryViewSet, basename='category')
router.register('all_category', AllCategoryViewSet, basename='all_category')
router.register('specification', SpecificationViewSet)
router.register('specification_value', SpecificationValueViewSet)
router.register('items', ItemViewSet, basename='items')
router.register('all_items', AllItemViewSet, basename='all_items')
router.register('request', RequestViewSet, basename='request')
router.register('all_request', AllRequestViewSet, basename='all_request')

urlpatterns = [
    path('', include(router.urls)),
]