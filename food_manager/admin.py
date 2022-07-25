from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Category, Tag, Food


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Food)