from django.urls import path, include

from wind_simulation_model.views import (
    wind_station_simulation_main, wind_station_simulation_now, wind_station_simulation_forecast,
    calculate_solar_radiation, get_forecast_data, turbines, turbine_in_detail, add_turbine,
    edit_turbine, edit_turbine_field, delete_turbine_table, add_turbine_field, get_all_forecast_data,
    thermal_energy_simulation_main, thermal_energy_boiler, thermal_energy_cogeneration_plant,
    thermal_energy_heat_pump, thermal_energy_regenerative_heat_exchanger, get_boiler_calculations,
    get_cogeneration_plant_calculations, get_heat_pump_calculations, get_regenerative_heat_exchanger_calculations
)


urlpatterns = [
    # Сонячна станція
    path('solar_radiation', calculate_solar_radiation, name='calculate_solar_radiation'),

    # Імітаційна модель вітрової станції ################
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

    path('get_boiler_calculations', get_boiler_calculations, name='get_boiler_calculations'),
    path('get_cogeneration_plant_calculations', get_cogeneration_plant_calculations, name='get_cogeneration_plant_calculations'),
    path('get_heat_pump_calculations', get_heat_pump_calculations, name='get_heat_pump_calculations'),
    path('get_regenerative_heat_exchanger_calculations', get_regenerative_heat_exchanger_calculations, name='get_regenerative_heat_exchanger_calculations'),

    # Обладнання
    path('thermal_energy_simulation', thermal_energy_simulation_main, name='thermal_energy_simulation'),
    path('thermal_energy_simulation/boiler', thermal_energy_boiler, name='thermal_energy_boiler'),
    path('thermal_energy_simulation/cogeneration_plant', thermal_energy_cogeneration_plant, name='thermal_energy_cogeneration_plant'),
    path('thermal_energy_simulation/heat_pump', thermal_energy_heat_pump, name='thermal_energy_heat_pump'),
    path('thermal_energy_simulation/regenerative_heat_exchanger', thermal_energy_regenerative_heat_exchanger, name='thermal_energy_regenerative_heat_exchanger'),
]
