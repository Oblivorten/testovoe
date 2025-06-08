from django.shortcuts import render, redirect
from .models import Truck, Warehouse, Unload
from shapely.wkt import loads
from shapely.geometry import Point


def unload(request):
    trucks = Truck.objects.all()
    warehouse = Warehouse.objects.first()
    polygon = loads(warehouse.polygon)
    if request.method == 'POST':
        weight_before = warehouse.weight
        warehouse.weight_before_unload = weight_before
        warehouse.save()
        total_weight = weight_before
        total_sio2 = warehouse.sio2_percent * weight_before
        total_fe = warehouse.fe_percent * weight_before
        for truck in trucks:
            coords = request.POST.get(f'truck_{truck.id}_coords', '').strip()
            try:
                x, y = map(float, coords.split())
            except ValueError:
                continue
            point = Point(x, y)
            is_inside = polygon.contains(point) or polygon.touches(point)
            if is_inside:
                total_weight += truck.weight
                total_sio2 += truck.sio2_percent * truck.weight
                total_fe += truck.fe_percent * truck.weight
                Unload.objects.create(
                    truck=truck,
                    warehouse=warehouse,
                    x_coord=x,
                    y_coord=y,
                    is_successful=True,
                )
            else:
                Unload.objects.create(
                    truck=truck,
                    warehouse=warehouse,
                    x_coord=x,
                    y_coord=y,
                    is_successful=False,
                )
        warehouse.weight = total_weight
        warehouse.sio2_percent = total_sio2 / total_weight if total_weight > 0 else 0
        warehouse.fe_percent = total_fe / total_weight if total_weight > 0 else 0
        warehouse.weight_after_unload = total_weight
        warehouse.save()
    context = {
        'trucks': trucks,
        'warehouse': warehouse,
    }
    return render(request, 'warehouse/unload.html', context)


def clear_warehouse(request):
    Unload.objects.all().delete()
    warehouse = Warehouse.objects.first()
    warehouse.weight = 0
    warehouse.sio2_percent = 0
    warehouse.fe_percent = 0
    warehouse.weight_before_unload = 0
    warehouse.weight_after_unload = 0
    warehouse.save()
    return redirect('unload')
