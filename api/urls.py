from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CustomerViewSet, RepairViewSet, InvoiceViewSet, login_user, get_settings

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'repairs', RepairViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_user, name='login'),
    path('settings/', get_settings, name='settings'),
]
