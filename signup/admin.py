from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Unregister the original User model
admin.site.unregister(User)

# Register the custom UserAdmin
admin.site.register(User, UserAdmin)
