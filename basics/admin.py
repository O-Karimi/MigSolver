from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category

# Register the Custom User using Django's built-in UserAdmin layout
admin.site.register(User, UserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}