from django.contrib import admin

from .models import CouponModel, CouponUsageModel


admin.site.register(CouponModel)
admin.site.register(CouponUsageModel)
