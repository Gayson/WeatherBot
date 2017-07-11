<?php

//$data = $argv[2];

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
        <img src="lib/title.png" width="350px" height="200px">
        <div class="title">
            <div class="otherInfo">
                <span class="city"></span>
                <span class="date"></span>
            </div>
            <div class="weatherInfo">
                <div class="tempDiv">
                    <i class="wi wi-thermometer"></i>
                    <span class="maxTemp"></span>&#176;&nbsp;/
                    <span class="minTemp"></span>&#176;
                </div>
                <div class="weatherDiv">
                    <div class="weather"><i class="wi"></i></div>
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
<script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
<script src="https://cdn.bootcss.com/html2canvas/0.5.0-beta4/html2canvas.min.js"></script>
<script src="js/index.js"></script>
</html>