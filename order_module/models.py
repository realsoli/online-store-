from django.db import models
from account_module.models import User
from product_module.models import Product


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='نهایی شده/نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return str(self.user)

    def calculate_total_price(self):
        total_amount = 0

        for item in self.orderdetail_set.all():
            price = item.final_price or item.product.price
            total_amount += price * item.count

        return total_amount

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    count = models.PositiveIntegerField(verbose_name='تعداد')

    def get_total_price(self):
        # اگر final_price موجود بود از آن استفاده می‌کنیم
        # در غیر اینصورت قیمت محصول را در نظر می‌گیریم
        price = self.final_price or (self.product.price if self.product else 0)
        return price * self.count
    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'
