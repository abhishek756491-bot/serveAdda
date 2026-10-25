from django.contrib import admin
from .models import User, SubscriptionPlan, Tenant

admin.site.register(User)
admin.site.register(SubscriptionPlan)
admin.site.register(Tenant)