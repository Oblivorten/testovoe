from django.db import models


class Truck(models.Model):
    number = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=25)
    lifting_capacity = models.IntegerField()
    weight = models.IntegerField()
    sio2_percent = models.FloatField()
    fe_percent = models.FloatField()

    @property
    def overload(self):
        if self.weight > self.lifting_capacity:
            return round((self.weight - self.lifting_capacity) / self.lifting_capacity * 100, 2)
        return 0

    def __str__(self):
        return self.model


class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    polygon = models.TextField(default='POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))')
    weight = models.IntegerField()
    sio2_percent = models.FloatField()
    fe_percent = models.FloatField()
    weight_before_unload = models.IntegerField(null=True, blank=True)
    weight_after_unload = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Unload(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    x_coord = models.FloatField()
    y_coord = models.FloatField()
    unload_time = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)