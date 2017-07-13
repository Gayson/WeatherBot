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
                <?php $dataObj->getWarning() ?>
            </div>
            <div class="weatherInfo">
                <div class="tempDiv">
                    <i class="wi wi-thermometer"></i>
                    <span class="maxTemp"><?php $dataObj->getMaxTemp() ?></span>&#176;&nbsp;/
                    <span class="minTemp"><?php $dataObj->getMinTemp() ?></span>&#176;
                    <div class="aqiDiv">AQI:
                        <span class="aqi"><?php $dataObj->getAqi() ?></span>&nbsp;
                        <span class="aqiQuality"><?php $dataObj->getAqiQuality() ?></span>
                    </div>
                </div>
                <div class="weatherDiv">
                    <div class="weather"><?php $dataObj->getWeather() ?></div>
                    <div class="wind"><?php $dataObj->getWind() ?></div>
                    <div class="humidity"><?php $dataObj->getHumidity() ?>%</div>
                </div>
            </div>
        </div>
        <div class="body">
            <div class="living">
                <span class="livingIndex"><?php $dataObj->getLivingIndex(0) ?></span>
                <span class="livingValue"><?php $dataObj->getLivingValue(0) ?></span>
                <span class="livingAdvice"><?php $dataObj->getLivingAdvice(0) ?></span>
            </div>
            <div class="living">
                <span class="livingIndex"><?php $dataObj->getLivingIndex(1) ?></span>
                <span class="livingValue"><?php $dataObj->getLivingValue(1) ?></span>
                <span class="livingAdvice"><?php $dataObj->getLivingAdvice(1) ?></span>
            </div>
            <div class="living">
                <span class="livingIndex"><?php $dataObj->getLivingIndex(2) ?></span>
                <span class="livingValue"><?php $dataObj->getLivingValue(2) ?></span>
                <span class="livingAdvice"><?php $dataObj->getLivingAdvice(2) ?></span>
            </div>
        </div>
    </div>
</body>


</html>