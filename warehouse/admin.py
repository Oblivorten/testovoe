from django.contrib import admin
from .models import Truck, Warehouse


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    fields = ('number', 'model', 'lifting_capacity', 'weight', 'sio2_percent', 'fe_percent')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    fields = ('name', 'polygon', 'weight', 'sio2_percent', 'fe_percent')
