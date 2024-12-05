import uuid
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "pending"),
        ('processed', 'processed'),
        ('cancelled', 'cancelled'),
    ]
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.status == 'pending' and Order.objects.filter(user=self.user, status='pending').exists():
            raise ValueError('A user can have only one pending order.')
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.id} - {self.status}"

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart_items')
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity} x {self.price}"
