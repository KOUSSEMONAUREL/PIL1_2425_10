from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RideOffer, RideRequest, Match, PrivateMessage

admin.site.register(CustomUser, UserAdmin)
admin.site.register(RideOffer)
admin.site.register(RideRequest)
admin.site.register(Match)
admin.site.register(PrivateMessage)
