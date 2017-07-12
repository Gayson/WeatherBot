<?php
function code2weather($code, &$weather, &$icon, &$imgPath)
{
    switch ($code) {
        case 0:
        case 1:
        case 2:
        case 3:
        case 4:
            $weather = '晴';
            $icon = '<i class="wi wi-day-sunny"></i>';
            $imgPath = 'lib/sunny.jpg';
            break;
        case 5:
        case 6:
        case 7:
        case 8:
            $weather = '多云';
            $icon = '<i class="wi wi-cloudy"></i>';
            $imgPath = 'lib/cloudy.jpg';
            break;
        case 9:
            $weather = '阴';
            $icon = '<i class="wi wi-cloud"></i>';
            $imgPath = 'lib/cloudy.jpg';
            break;
        case 10:
            $weather = '阵雨';
            $icon = '<i class="wi wi-showers"></i>';
            $imgPath = 'lib/rainy.jpg';
            break;
        case 11:
        case 12:
            $weather = '雷阵雨';
            $icon = '<i class="wi wi-storm-showers"></i>';
            $imgPath = 'lib/rainy.jpg';
            break;
        case 13:
            $weather = '小雨';
            $icon = '<i class="wi wi-sprinkle"></i>';
            $imgPath = 'lib/rainy.jpg';
            break;
        case 14:
            $weather = '中雨';
            $icon = '<i class="wi wi-rain"></i>';
            $imgPath = 'lib/rainy.jpg';
            break;
        case 15:
            $weather = '大雨';
            $icon = '<i class="wi wi-rain"></i>';
            $imgPath = 'lib/rainy.jpg';
            break;
        case 16:
            $weather = '暴雨';
            $icon = '<i class="wi wi-rain"></i>';
            $imgPath = 'lib/rainy.jpg';
            break;
        case 17:
            $weather = '大暴雨';
            $icon = '<i class="wi wi-rain"></i>';
            $imgPath = 'lib/rainy.jpg';
            break;
        case 18:
            $weather = '特大暴雨';
            $icon = '<i class="wi wi-rain"></i>';
            $imgPath = 'lib/rainy.jpg';
            break;
        case 19:
        case 20:
            $weather = '雨夹雪';
            $icon = '<i class="wi wi-sleet"></i>';
            $imgPath = 'lib/rainy.jpg';
            break;
        case 21:
        case 22:
            $weather = '小雪';
            $icon = '<i class="wi wi-snow"></i>';
            $imgPath = 'lib/snowy.jpg';
            break;
        case 23:
            $weather = '中雪';
            $icon = '<i class="wi wi-snow"></i>';
            $imgPath = 'lib/snowy.jpg';
            break;
        case 24:
            $weather = '大雪';
            $icon = '<i class="wi wi-snow"></i>';
            $imgPath = 'lib/snowy.jpg';
            break;
        case 25:
            $weather = '暴雪';
            $icon = '<i class="wi wi-snow"></i>';
            $imgPath = 'lib/snowy.jpg';
            break;
        case 26:
        case 27:
        case 28:
        case 29:
            $weather = '沙尘';
            $icon = '<i class="wi wi-dust"></i>';
            $imgPath = 'lib/cloudy.jpg';
            break;
        case 30:
        case 31:
            $weather = '雾霾';
            $icon = '<i class="wi wi-fog"></i>';
            $imgPath = 'lib/cloudy.jpg';
            break;
        case 32:
        case 33:
            $weather = '大风';
            $icon = '<i class="wi wi-windy"></i>';
            $imgPath = 'lib/cloudy.jpg';
            break;
        case 34:
        case 35:
            $weather = '飓风';
            $icon = '<i class="wi wi-hurricane"></i>';
            $imgPath = 'lib/cloudy.jpg';
            break;
        case 36:
            $weather = '龙卷风';
            $icon = '<i class="wi wi-tornado"></i>';
            $imgPath = 'lib/cloudy.jpg';
            break;
        default:
            $weather = '未知';
            $imgPath = 'lib/sunny.jpg';
            break;
    }
}