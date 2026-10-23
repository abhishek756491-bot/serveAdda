from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 1. Subscription Plans Model
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_services_limit = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 2. Tenants (Host Agencies) Model
class Tenant(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.RESTRICT)
    agency_name = models.CharField(max_length=150, unique=True)
    subdomain_slug = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=80)
    status = models.CharField(
        max_length=10, 
        choices=[('PENDING', 'Pending'), ('ACTIVE', 'Active'), ('BLOCKED', 'Blocked')], 
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agency_name

# 3. Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'SUPER_ADMIN')
        return self.create_user(email, full_name, password, **extra_fields)

# 4. Customized User Model
class User(AbstractBaseUser, PermissionsMixin):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=150, unique=True)
    role = models.CharField(
        max_length=20, 
        choices=[('SUPER_ADMIN', 'Super Admin'), ('HOST', 'Host'), ('CUSTOMER', 'Customer')], 
        default='CUSTOMER'
    )
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.role})"