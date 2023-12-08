from django.db import models


class WindTurbine(models.Model):
    name = models.CharField(max_length=100)
    wind_speed = models.FloatField()
    power_output = models.FloatField()

    def __str__(self):
        return self.name


class WindTurbineParameter(models.Model):
    name = models.CharField(max_length=100)
    rotor_area = models.FloatField()

    def __str__(self):
        return self.name
