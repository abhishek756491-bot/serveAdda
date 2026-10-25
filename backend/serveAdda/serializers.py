from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tenant

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tenant_slug = serializers.CharField(write_only=True, required=False) # Host ke liye tenant pass karne ka option

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'role', 'phone', 'tenant_slug')

    def create(self, validated_data):
        tenant_slug = validated_data.pop('tenant_slug', None)
        tenant = None
        
        # Agar Host register kar raha hai, toh uski agency (tenant) find karein
        if tenant_slug:
            try:
                tenant = Tenant.objects.get(subdomain_slug=tenant_slug)
            except Tenant.DoesNotExist:
                raise serializers.ValidationError({"error": "Invalid Tenant Subdomain"})

        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            role=validated_data.get('role', 'CUSTOMER'),
            phone=validated_data.get('phone', ''),
            tenant=tenant
        )
        return user