<?php

require './php/getData.php';


?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="css/index.css">
    <link rel="stylesheet" href="css/weather-icons.min.css">
</head>
<body>
    <div class="img">
        <img src="<?php $dataObj->getImgPath() ?>" width="350px" height="200px">
        <div class="title">
            <div class="otherInfo">
                <span class="location"><?php $dataObj->getLocation() ?></span>
                <span class="date"><?php $dataObj->getDate() ?></span>
                <span class="warning"><?php $dataObj->getWarning() ?></span>
            </div>
            <div class="weatherInfo">
                <div class="tempDiv">
                    <i class="wi wi-thermometer"></i>
                    <span class="maxTemp"><?php $dataObj->getMaxTemp() ?></span>&#176;&nbsp;/
                    <span class="minTemp"><?php $dataObj->getMinTemp() ?></span>&#176;
                    <div class="aqiDiv">AQI:<span class="aqi"><?php $dataObj->getAqi() ?></span></div>
                </div>
                <div class="weatherDiv">
                    <div class="weather"><?php $dataObj->getWeather() ?></div>
                    <div class="wind"><?php $dataObj->getWind() ?></div>
                </div>
            </div>
        </div>
        <div class="body">
            <div class="living">
                <span class="livingIndex"></span>
                <span class="livingValue"></span>
                <span class="livingAdvice"></span>
            </div>
            <div class="living">
                <span class="livingIndex"></span>
                <span class="livingValue"></span>
                <span class="livingAdvice"></span>
            </div>
            <div class="living">
                <span class="livingIndex"></span>
                <span class="livingValue"></span>
                <span class="livingAdvice"></span>
            </div>
        </div>
    </div>
</body>


</html>