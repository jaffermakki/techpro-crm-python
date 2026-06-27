from django.db import models
from django.contrib.auth.models import User
import uuid

def uid():
    return 'id_' + str(uuid.uuid4()).replace('-', '')[:12]

class Product(models.Model):
    CAT_CHOICES = [
        ('CASE','Case'), ('CHARGER','Charger'), ('CABLE','Cable'),
        ('SCREEN','Screen'), ('BATTERY','Battery'),
        ('ACCESSORY','Accessory'), ('PART','Part')
    ]
    id = models.CharField(max_length=50, primary_key=True, default=uid, editable=False)
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CAT_CHOICES)
    subcategory = models.CharField(max_length=50, blank=True)
    shelf = models.CharField(max_length=20, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    threshold = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Customer(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uid, editable=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    points = models.IntegerField(default=0)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    store_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_visit = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

class Repair(models.Model):
    STATUS_CHOICES = [
        ('RECEIVED','Received'), ('DIAGNOSED','Diagnosed'), ('WAITING','Waiting'),
        ('IN_PROGRESS','In Progress'), ('READY','Ready'),
        ('COMPLETED','Completed'), ('COLLECTED','Collected')
    ]
    id = models.CharField(max_length=50, primary_key=True, default=uid, editable=False)
    ticket_no = models.IntegerField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECEIVED')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    device = models.CharField(max_length=100)
    issue = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    approved_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    warranty_days = models.IntegerField(default=90)
    promised_by = models.DateField(null=True, blank=True)
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    parts_used = models.JSONField(default=list)
    status_history = models.JSONField(default=list)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Invoice(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uid, editable=False)
    number = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20, blank=True)
    customer_email = models.EmailField(blank=True)
    province = models.CharField(max_length=5, default='ON')
    lines = models.JSONField(default=list)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_lines = models.JSONField(default=list)
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment = models.CharField(max_length=50)
    tendered = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=20, default='SALE')
    original_invoice = models.CharField(max_length=50, blank=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ShopSettings(models.Model):
    shop_name = models.CharField(max_length=100, default='Tech-Pro+')
    shop_address = models.TextField(blank=True)
    shop_phone = models.CharField(max_length=20, blank=True)
    shop_email = models.EmailField(blank=True)
    province = models.CharField(max_length=5, default='ON')
    shop_gst = models.CharField(max_length=50, blank=True)
    shop_pst = models.CharField(max_length=50, blank=True)
    currency = models.CharField(max_length=5, default='$')
    invoice_prefix = models.CharField(max_length=10, default='INV')
    next_invoice = models.IntegerField(default=1)
    cash_float = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    points_per_dollar = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    points_redeem_rate = models.IntegerField(default=100)
