function codeToWeather(code) {
    var $weather = $('.weather');
    var $img = $('.img img');
    switch (code) {
        case 0:
        case 1:
        case 2:
        case 3:
        case 4:
            $weather.text('晴').prepend('<i class="wi wi-day-sunny"></i>');
            $img.prop('src', 'lib/sunny.jpg');
            break;
        case 5:
        case 6:
        case 7:
        case 8:
            $weather.text('多云').prepend('<i class="wi wi-cloudy"></i>');
            $img.prop('src', 'lib/cloudy.jpg');
            break;
        case 9:
            $weather.text('阴').prepend('<i class="wi wi-cloud"></i>');
            $img.prop('src', 'lib/cloudy.jpg');
            break;
        case 10:
            $weather.text('阵雨').prepend('<i class="wi wi-showers"></i>');
            $img.prop('src', 'lib/rainy.jpg');
            break;
        case 11:
        case 12:
            $weather.text('雷阵雨').prepend('<i class="wi wi-storm-showers"></i>');
            $img.prop('src', 'lib/rainy.jpg');
            break;
        case 13:
            $weather.text('小雨').prepend('<i class="wi wi-sprinkle"></i>');
            $img.prop('src', 'lib/rainy.jpg');
            break;
        case 14:
            $weather.text('中雨').prepend('<i class="wi wi-rain"></i>');
            $img.prop('src', 'lib/rainy.jpg');
            break;
        case 15:
            $weather.text('大雨').prepend('<i class="wi wi-rain"></i>');
            $img.prop('src', 'lib/rainy.jpg');
            break;
        case 16:
            $weather.text('暴雨').prepend('<i class="wi wi-rain"></i>');
            $img.prop('src', 'lib/rainy.jpg');
            break;
        case 17:
            $weather.text('大暴雨').prepend('<i class="wi wi-rain"></i>');
            $img.prop('src', 'lib/rainy.jpg');
            break;
        case 18:
            $weather.text('特大暴雨').prepend('<i class="wi wi-rain"></i>');
            $img.prop('src', 'lib/rainy.jpg');
            break;
        case 19:
        case 20:
            $weather.text('雨夹雪').prepend('<i class="wi wi-sleet"></i>');
            $img.prop('src', 'lib/rainy.jpg');
            break;
        case 21:
        case 22:
            $weather.text('小雪').prepend('<i class="wi wi-snow"></i>');
            $img.prop('src', 'lib/snowy.jpg');
            break;
        case 23:
            $weather.text('中雪').prepend('<i class="wi wi-snow"></i>');
            $img.prop('src', 'lib/snowy.jpg');
            break;
        case 24:
            $weather.text('大雪').prepend('<i class="wi wi-snow"></i>');
            $img.prop('src', 'lib/snowy.jpg');
            break;
        case 25:
            $weather.text('暴雪').prepend('<i class="wi wi-snow"></i>');
            $img.prop('src', 'lib/snowy.jpg');
            break;
        case 26:
        case 27:
        case 28:
        case 29:
            $weather.text('沙尘').prepend('<i class="wi wi-dust"></i>');
            $img.prop('src', 'lib/cloudy.jpg');
            break;
        case 30:
        case 31:
            $weather.text('雾霾').prepend('<i class="wi wi-fog"></i>');
            $img.prop('src', 'lib/cloudy.jpg');
            break;
        case 32:
        case 33:
            $weather.text('大风').prepend('<i class="wi wi-windy"></i>');
            $img.prop('src', 'lib/cloudy.jpg');
            break;
        case 34:
        case 35:
            $weather.text('飓风').prepend('<i class="wi wi-hurricane"></i>');
            $img.prop('src', 'lib/cloudy.jpg');
            break;
        case 36:
            $weather.text('龙卷风').prepend('<i class="wi wi-tornado"></i>');
            $img.prop('src', 'lib/cloudy.jpg');
            break;
        default:
            $weather.text('未知');
            $img.prop('src', 'lib/sunny.jpg');
            break;

    }
}
