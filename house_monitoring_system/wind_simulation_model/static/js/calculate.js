function calculateTimeAngleOfSun(longitude, N) {
    // Визначимо поточний час в годинах
    var currentDate = new Date();
    var t = currentDate.getHours();

    // Різниця між місцевим офіційним та середнім часом за Грінвічем
    const now = new Date();
    const utcString = now.toUTCString();
    const grinvichTime = parseInt(utcString.slice(17,19));
    var Tutc = Math.abs(t - grinvichTime);

    var B = 0.986 * N - 79.866;
    var Tuv = 0.11 * Math.sin(2 * B) - 0.08 * Math.cos(B) - Math.sin(B);

    var W = 15 * (t - 12 - Tuv - Tutc) + longitude;

    return W;
}


function calculateDayNumber(userDate) {
    const date = new Date(userDate); 
    const startOfYear = new Date(date.getFullYear(), 0, 0);
    const diff = date - startOfYear;
    const oneDay = 1000 * 60 * 60 * 24;

    return Math.floor(diff / oneDay);
}


function block_1(latitude, betta, gamma, N, W, direct_solar_radiation) {
    var A = Math.sin(latitude) * Math.cos(betta);
    var B = Math.cos(latitude) * Math.sin(betta) * Math.cos(gamma);
    var C = Math.sin(betta) * Math.sin(gamma);
    var D = Math.cos(latitude) * Math.cos(betta);
    var E = Math.sin(latitude) * Math.sin(betta) * Math.cos(gamma);

    // Кутове схилення Сонця
    var angular_declination_of_sun = 23.45 * Math.sin(0.986 * N + 280.024);

    var latitude = latitude * Math.PI / 180; 
    var angular_declination_of_sun = angular_declination_of_sun * Math.PI / 180;
    var W = W * Math.PI / 180;

    var cos_teta = (A - B) * Math.sin(angular_declination_of_sun) + (C * Math.sin(W)+ (D + E) * Math.cos(W));

    var cos_teta_z = Math.acos(
        Math.sin(angular_declination_of_sun) * Math.sin(latitude) + Math.cos(latitude) - Math.cos(angular_declination_of_sun) * Math.cos(W)
    );

    var result = direct_solar_radiation * cos_teta / cos_teta_z;

    return result;
}


function block_2(scattered_solar_radiation, betta) {
    var result = scattered_solar_radiation * (1 + Math.cos(betta)) / 2;
    return result
}


function block_3(total_solar_radiation, albedo, betta) {
    var result = albedo * total_solar_radiation * (1 - Math.cos(betta)) / 2;
    return result
}


document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('solarCalculationData');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Отримуємо значення полів форми
        var latitude = form.elements.latitude.value;
        var longitude = form.elements.longitude.value;
        var date = form.elements.date.value;
        var betta = form.elements.betta.value;
        var gamma = form.elements.gamma.value;
        var albedo = form.elements.albedo.value;

        var direct_solar_radiation = form.elements.direct_solar_radiation.value;
        var scattered_solar_radiation = form.elements.scattered_solar_radiation.value;
        var total_solar_radiation = form.elements.total_solar_radiation.value

        // Номер календарного дня з початку року
        var N = calculateDayNumber(date);
        
        // Часовий кут Сонця
        var W = calculateTimeAngleOfSun(longitude, N);
        
        var b1 = block_1(latitude, betta, gamma, N, W, direct_solar_radiation);
        var b2 = block_2(scattered_solar_radiation, betta);
        var b3 = block_3(total_solar_radiation, albedo, betta);

        var final_result = b1 + b2 + b3;
        console.log('Фінальний результат: ', final_result);

        function updateResult(value) {
            const resultElement = document.getElementById('resultDataTable');
            resultElement.innerHTML = value.toFixed(2) + ' Вт/м^2';
        }
          
        updateResult(final_result);
    });
});
