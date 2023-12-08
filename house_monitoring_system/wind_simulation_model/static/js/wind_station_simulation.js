function calculateCapacity(temperature, windSpeed, airPressure) {

}


$(document).ready(function(){
    $(".getForecast").submit(function(e){
        e.preventDefault();

        var inputCity = $('.city');

        $.ajax({
            type:'POST',
            url: '/get_forecast_data',
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'city': inputCity.val(),
            },
            success: function(response) {
                console.log(response);
                $(".tableCity").text(response.city);
                $(".temperature").text(response.temperature);
                $(".airPressure").text(response.airPressure);
                $(".windSpeed").text(response.windSpeedText);
                $(".capacity").text(response.capacity);
            },
            error: function(response){
                console.log('error');
            }
        });
    });
});


