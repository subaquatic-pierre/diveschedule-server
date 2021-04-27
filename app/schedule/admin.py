from django.contrib import admin
from .models.booking import Booking


class BookingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Booking, BookingAdmin)