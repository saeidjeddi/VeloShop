from django.db import models
from django.conf import settings
from django.utils import timezone



class CouponModel(models.Model):
    code = models.CharField(max_length=50, unique=True, db_index=True,)
    discount = models.PositiveSmallIntegerField(default=0)
    max_uses = models.PositiveIntegerField(default=1, )
    used_count = models.PositiveIntegerField(default=0,)
    is_active = models.BooleanField(default=True,)
    valid_from = models.DateTimeField(null=True, blank=True,)
    valid_until = models.DateTimeField(null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True,)
    
    def __str__(self):
        return self.code
    
    
    @property
    def is_valid(self):
        now = timezone.now()
        
        if not self.is_active:
            return False
        
        if self.used_count >= self.max_uses:
            return False
        
        if self.valid_from and now < self.valid_from:
            return False

        if self.valid_until and now > self.valid_until:
            return False
        
        return True
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'coupons'
        
    

class CouponUsageModel(models.Model):
    coupon = models.ForeignKey(CouponModel, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coupon_usages_user')
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coupon_usages'
        
        constraints = [
            models.UniqueConstraint(fields=['coupon', 'user'], name='unique_coupon_usage')
        ]
        
        
    def __str__(self):
        return f"{self.coupon.code} - {self.user.username}"