import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    
    class Meta:
        verbose_name = ('カテゴリ')
        verbose_name_plural = ('カテゴリ')
    
    def __str__(self):
        return self.category_name


class Tag(models.Model):
    tag_name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    
    class Meta:
        verbose_name = ('タグ')
        verbose_name_plural = ('タグ')

    def __str__(self):
        return self.tag_name


class Food(models.Model):
    food_name = models.CharField(max_length=30)
    tags = models.ManyToManyField(Tag, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    trash = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('食品')
        verbose_name_plural = ('食品')
    
    def __str__(self):
        return self.food_name
    
    def expiration_date(self):
        now = timezone.now()
        output = None
        if self.date is not None:
            if self.date - datetime.timedelta(days=3) <= now < self.date:
                output = 'near'
            elif now >= self.date:
                output = 'expired'
        return output