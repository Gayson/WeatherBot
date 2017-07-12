<?php

$data = $argv[1];
echo $data;
//echo "<script type='text/javascript'>getData($data);</script>";
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
        <img src="lib/sunny.jpg" width="350px" height="200px">
        <div class="title">
            <div class="otherInfo">
                <span class="location"></span>
                <span class="date"></span>
                <span class="warning"></span>
            </div>
            <div class="weatherInfo">
                <div class="tempDiv">
                    <i class="wi wi-thermometer"></i>
                    <span class="maxTemp"></span>&#176;&nbsp;/
                    <span class="minTemp"></span>&#176;
                    <div class="aqiDiv">AQI:<span class="aqi"></span></div>
                </div>
                <div class="weatherDiv">
                    <div class="weather"></div>
                    <div class="wind"></div>
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

<script src="bundle.js"></script>
</html>