from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import Product, Customer, Repair, Invoice, ShopSettings
from .serializers import *
from .utils import calc_canadian_tax
import uuid
from decimal import Decimal

def uid():
    return 'id_' + str(uuid.uuid4()).replace('-', '')[:12]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not serializer.validated_data.get('id'):
            serializer.save(id=uid())

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def complete_sale(self, request):
        data = request.data
        cart = data.get('cart', [])
        if not cart:
            return Response({'error': 'Cart empty'}, status=400)

        subtotal = sum(Decimal(item['price']) * int(item['qty']) for item in cart)
        discount = Decimal(data.get('discount', 0))
        taxable = max(Decimal(0), subtotal - discount)
        province = data.get('province', 'ON')
        tax_result = calc_canadian_tax(taxable, province)
        total = tax_result['total']

        customer_id = data.get('customerId')
        customer = Customer.objects.filter(id=customer_id).first()
        if not customer and data.get('customerName') and data.get('customerPhone'):
            customer = Customer.objects.create(
                id=uid(),
                name=data['customerName'],
                phone=data['customerPhone'],
                email=data.get('customerEmail', '')
            )

        for item in cart:
            try:
                prod = Product.objects.get(id=item['productId'])
                prod.stock = max(0, prod.stock - int(item['qty']))
                prod.save()
            except Product.DoesNotExist:
                pass

        if customer:
            customer.spent += total
            customer.points += int(total * Decimal(1))
            customer.store_credit -= Decimal(data.get('store_credit_used', 0))
            customer.last_visit = data.get('date', '2025-01-01')
            customer.save()

        settings = ShopSettings.objects.first()
        if not settings:
            settings = ShopSettings.objects.create()

        invoice_no = f"{settings.invoice_prefix}-{settings.next_invoice:04d}"
        settings.next_invoice += 1
        settings.save()

        invoice = Invoice.objects.create(
            id=uid(),
            number=invoice_no,
            customer=customer,
            customer_name=data.get('customerName', 'Walk-in'),
            customer_phone=data.get('customerPhone', ''),
            province=province,
            lines=cart,
            subtotal=subtotal,
            discount=discount,
            tax_lines=tax_result['lines'],
            gst=tax_result['gst'],
            pst=tax_result['pst'],
            hst=tax_result['hst'],
            total_tax=sum(Decimal(l['amount']) for l in tax_result['lines']),
            total=total,
            payment=data.get('payment', 'Cash'),
            tendered=Decimal(data.get('tendered', 0)),
            change_amount=max(Decimal(0), Decimal(data.get('tendered', 0)) - total),
            staff=request.user,
            type='SALE'
        )

        return Response(InvoiceSerializer(invoice).data, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({'status': 'ok', 'name': user.username, 'role': 'staff'})
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_settings(request):
    settings, _ = ShopSettings.objects.get_or_create()
    if request.method == 'POST':
        serializer = SettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    return Response(SettingsSerializer(settings).data)
