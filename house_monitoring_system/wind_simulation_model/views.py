from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import OuterRef, Subquery

from wind_simulation_model.scrap_data import get_local_data, get_local_data_forecast
from .models import WindTurbine, WindTurbineParameter


def calculate_solar_radiation(request):
    return render(
        request=request,
        template_name='wind_simulation_model/calculate_solar_radiation.html'
    )


def wind_station_simulation_main(request):
    data = get_local_data('київ')

    return render(
        request=request,
        template_name='wind_simulation_model/wind_station_simulation_main.html',
        context=data
    )


def wind_station_simulation_now(request):
    data = get_local_data('київ')
    data['list_of_turbines'] = set(WindTurbine.objects.values_list('name', flat=True))

    return render(
        request=request,
        template_name='wind_simulation_model/wind_station_simulation_now.html',
        context=data
    )


def wind_station_simulation_forecast(request):
    data = get_local_data('київ')
    data['list_of_turbines'] = set(WindTurbine.objects.values_list('name', flat=True))

    return render(
        request=request,
        template_name='wind_simulation_model/wind_station_simulation_forecast.html',
        context=data
    )


def turbines(request):
    list_of_turbines = WindTurbine.objects.values('name').annotate(
        id=Subquery(
            WindTurbine.objects.filter(name=OuterRef('name')).order_by('id').values('id')[:1]
        )
    ).distinct()

    data = {'list_of_turbines': list_of_turbines}

    return render(
        request=request,
        template_name='wind_simulation_model/wind_turbines.html',
        context=data
    )


def turbine_in_detail(request, turbine_id):
    print(turbine_id)
    turbine_name = WindTurbine.objects.values_list('name', flat=True).get(id=turbine_id)
    print(turbine_name)
    all_turbine_chars = WindTurbine.objects.all().filter(name=turbine_name)

    data = {
        'turbine_id': turbine_id,
        'turbine_name': turbine_name,
        'all_strings': all_turbine_chars
    }

    return render(
        request=request,
        template_name='wind_simulation_model/wind_turbine_in_detail.html',
        context=data
    )


def add_turbine(request):
    if request.method == 'POST':
        name_of_turbine = request.POST.get('nameOfTurbine')
        rotor_area = request.POST.get('rotorArea')
        wind_speed = request.POST.get('windSpeed')
        capacity = request.POST.get('capacity')

        new_turbine = WindTurbine(
            name=name_of_turbine,
            wind_speed=wind_speed,
            power_output=capacity
        )
        new_turbine.save()

        new_turbine = WindTurbineParameter(
            name=name_of_turbine,
            rotor_area=rotor_area
        )
        new_turbine.save()

        return redirect('list_of_turbines')

    return render(
        request=request,
        template_name='wind_simulation_model/add_turbine.html'
    )


def add_turbine_field(request, turbine_id):
    turbine_name = WindTurbine.objects.values_list('name', flat=True).get(id=turbine_id)

    if request.method == 'POST':
        wind_speed = request.POST.get('windSpeed')
        capacity = request.POST.get('capacity')

        new_turbine = WindTurbine(
            name=turbine_name,
            wind_speed=wind_speed,
            power_output=capacity
        )
        new_turbine.save()
        return redirect(f'/wind_simulation/list_of_turbines/{turbine_id}')

    return render(
        request=request,
        template_name='wind_simulation_model/add_turbine_field.html'
    )


def edit_turbine(request, turbine_id):
    turbine_name = WindTurbine.objects.values_list('name', flat=True).get(id=turbine_id)
    all_turbine_chars = WindTurbine.objects.all().filter(name=turbine_name)

    data = {
        'turbine_id': turbine_id,
        'turbine_name': turbine_name,
        'all_strings': all_turbine_chars
    }

    return render(
        request=request,
        template_name='wind_simulation_model/edit_turbine.html',
        context=data
    )


def edit_turbine_field(request, turbine_id, field_id):
    # if turbine_id == field_id:
    #     ...
    # else:

    if request.method == 'POST':
        wind_speed = request.POST.get('windSpeed')
        capacity = request.POST.get('capacity')

        WindTurbine.objects.filter(id=field_id).update(
            wind_speed=wind_speed,
            power_output=capacity
        )

        return redirect(f'/wind_simulation/list_of_turbines/{turbine_id}/edit')

    turbine_name = WindTurbine.objects.values_list('name', flat=True).get(id=turbine_id)
    all_turbine_chars = WindTurbine.objects.all().filter(name=turbine_name)

    data = {
        'turbine_id': turbine_id,
        'turbine_name': turbine_name,
        'all_strings': all_turbine_chars
    }

    return render(
        request=request,
        template_name='wind_simulation_model/edit_turbine_form.html',
        context=data
    )


def delete_turbine_table(request, turbine_id):
    turbine_name = WindTurbine.objects.values_list('name', flat=True).get(id=turbine_id)
    WindTurbine.objects.filter(name=turbine_name).delete()

    return redirect(f'/wind_simulation/list_of_turbines')


def delete_turbine():
    ...


def calculate_capacity(air_pressure, temperature, wind_speed, turbine_name):
    M = 29      # г / моль - молярна маса повітря
    R = 8.314   # Дж / (моль⋅К) - газова стала
    A = 7850  # площа ротора складає 7850 м^2
    # print(WindTurbineParameter.objects.filter(turbine_name=turbine_name).rotor_area)

    # Обчислимо щільність повітря
    ro = (M * (air_pressure * 133.33/1000)) / (R * temperature)

    capacity_instance = WindTurbine.objects.filter(name=turbine_name, wind_speed=float(int(wind_speed))).first()
    rotor_area_instance = WindTurbineParameter.objects.filter(name=turbine_name).first()

    if not capacity_instance:
        print('error')
        return False

    capacity = capacity_instance.power_output
    rotor_area = rotor_area_instance.rotor_area

    Cp = (capacity * 1000) / (rotor_area * (0.5 * ro * wind_speed**3))   # коефіцієнт
    Cp = int(Cp * 100) / 100

    power_plant_capacity = (0.5 * ro * rotor_area * (wind_speed**3) * Cp) / 1000
    print(f'result = {power_plant_capacity}')

    return power_plant_capacity


def create_parameters_table(turbine_name):
    all_turbine_chars = WindTurbine.objects.all().filter(name=turbine_name)

    table = '<table>'
    for turbine in all_turbine_chars:
        table += f'<tr><td>{turbine.wind_speed}</td><td class="tableCity">{turbine.power_output}</td></tr>'
    table += '</table>'

    return table


def get_forecast_data(request):
    city = request.POST['city']
    turbine_name = request.POST['turbine_name']
    data = get_local_data(city)

    result = calculate_capacity(
        air_pressure=data['airPressure'],
        temperature=data['temperature'] + 273,
        wind_speed=data['windSpeedNum'],
        turbine_name=turbine_name,
    )

    data['capacity'] = result
    data['city'] = city
    data['turbine_name'] = turbine_name
    data['parameters_table'] = create_parameters_table(turbine_name)

    return JsonResponse(data)


def get_all_forecast_data(request):
    city = request.POST['city']
    turbine_name = request.POST.get('turbine_name')
    date_1 = request.POST['date_1']
    date_2 = request.POST['date_2']

    data = {'city': city}
    result = get_local_data_forecast(city, turbine_name, date_1, date_2)

    data['result_table'] = result[0]
    data['total_capacity'] = result[1]

    print(data)
    return JsonResponse(data)
