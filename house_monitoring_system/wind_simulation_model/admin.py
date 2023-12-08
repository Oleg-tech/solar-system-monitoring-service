from django.contrib import admin
from .models import WindTurbine, WindTurbineParameter


admin.site.register(WindTurbine)
admin.site.register(WindTurbineParameter)
