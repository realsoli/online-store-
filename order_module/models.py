from django.db import models
from account_module.models import User
from product_module.models import Product


# Create your models here.

def calculate_total_price(self):
    total_amount = 0

    for order_detail in self.orderdetail_set.all():
        count = order_detail.count or 0

        if self.is_paid:
            price = order_detail.final_price or 0
        else:
            price = order_detail.product.price if order_detail.product and order_detail.product.price else 0

        total_amount += price * count

    return total_amount


    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        return self.count * self.product.price

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'
