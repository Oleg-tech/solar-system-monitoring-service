from django.urls import path, include

from wind_simulation_model.views import (
    wind_station_simulation_main, wind_station_simulation_now, wind_station_simulation_forecast,
    calculate_solar_radiation, get_forecast_data, turbines, turbine_in_detail, add_turbine,
    edit_turbine, edit_turbine_field, delete_turbine_table, add_turbine_field, get_all_forecast_data
)


urlpatterns = [
    path('solar_radiation', calculate_solar_radiation, name='calculate_solar_radiation'),

    path('wind_simulation', wind_station_simulation_main, name='wind_station_simulation_main'),
    path('wind_simulation/now', wind_station_simulation_now, name='wind_station_simulation_now'),
    path('wind_simulation/forecast', wind_station_simulation_forecast, name='wind_station_simulation_forecast'),

    path('wind_simulation/list_of_turbines', turbines, name='list_of_turbines'),
    path('wind_simulation/list_of_turbines/<int:turbine_id>', turbine_in_detail, name='turbine_ib_detail'),

    path('wind_simulation/add_turbine', add_turbine, name='add_turbine'),
    path('wind_simulation/list_of_turbines/<int:turbine_id>/add', add_turbine_field, name='add_turbine_field'),

    path('wind_simulation/list_of_turbines/<int:turbine_id>/edit', edit_turbine, name='edit_turbine'),
    path('wind_simulation/list_of_turbines/<int:turbine_id>/edit/<int:field_id>', edit_turbine_field, name='edit_turbine_field'),

    path('wind_simulation/list_of_turbines/<int:turbine_id>/delete', delete_turbine_table, name='delete_turbine_table'),

    path('get_forecast_data', get_forecast_data, name='get_forecast_data'),
    path('get_all_forecast_data', get_all_forecast_data, name='get_forecast_data'),
]
