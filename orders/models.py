from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Place(models.Model):
    REGIONS = (
        ('Andijon', _('Andijon'),),
        ('Buxoro', _('Buxoro')),
        ('Farg\'ona', _('Farg\'ona')),
        ('Jizzax', _('Jizzax')),
        ('Namangan', _('Namangan')),
        ('Navoiy', _('Navoiy')),
        ('Qashqadaryo', _('Qashqadaryo')),
        ('Qoraqalpog\'iston', _('Qoraqalpog\'iston')),
        ('Samarqand', _('Samarqand')),
        ('Sirdaryo', _('Sirdaryo')),
        ('Surxondaryo', _('Surxondaryo')),
        ('Toshkent vil.', _('Toshkent vil.')),
        ('Toshkent', _('Toshkent')),
        ('Xorazm', _('Xorazm')),
    )
    CITIES = (
    )
    region = models.CharField(max_length=150, blank=True, null=True, choices=REGIONS)
    city = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.region} - {self.city}"

class OrderImage(models.Model):
    # def get_upload_path(instance, filename):
        # return f"images/{instance.order.user}/{filename}"
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, null=True)
    
    def __str__(self) -> str:
        return f"Image {self.id}"

class Order(models.Model):
    STATUSES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='from_place', blank=True, null=True)
    to_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='to_place', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    car = models.CharField(max_length=150, blank=True, null=True)
    image = models.FileField(upload_to='images/%Y/%m/%d/', blank=True, null=True, default=None, )
    # image = models.ForeignKey(OrderImage, blank=True, null=True, on_delete=models.CASCADE, related_name='order_image')
    status = models.CharField(max_length=150, blank=True, null=True, choices=STATUSES)
    price = models.IntegerField(blank=True, null=True, default=0, help_text='Price in UZS')
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.from_place}->{self.to_place} - {self.date}"


class OrderHistory(models.Model):
    STATUSES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    from_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='from_place_history', blank=True, null=True)
    to_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='to_place_history', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='images/%Y/%m/%d/', blank=True, null=True)
    # image = models.ForeignKey(OrderImage, blank=True, null=True, on_delete=models.CASCADE)
    car = models.CharField(max_length=150, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True, default=0)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=100, choices=STATUSES, default='pending')


    def __str__(self) -> str:
        return f"{self.user} - {self.from_place}-{self.to_place} - {self.date}"
