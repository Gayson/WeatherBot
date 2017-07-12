<?php
try {
    global $argv;
    $parameter = $argv[1];
} catch (Exception $e) {
}

$dataObj = new Data;

require('util.php');

class Data {
    private $location, $date, $warning, $aqi, $maxTemp, $minTemp, $weather, $icon, $imgPath, $wind;
    private $livingIndex, $livingValue, $livingAdvice;

    function setData($jsonData) {
        $data = json_decode($jsonData);
        $this->location = $data->{'location'};
        $this->date = $data->{'date'};
        $this->warning = $data->{'warning'};
        $this->aqi = $data->{'aqi'};
        $this->maxTemp = $data->{'maxTemp'};
        $this->minTemp = $data->{'minTemp'};
        code2weather($data->{'weather'}, $this->weather, $this->icon, $this->imgPath);
        $this->wind = $data->{'wind'};
        //$this->livingIndex = json_decode($data->{'livingIndex'}, true);
        //$this->livingValue = json_decode($data->{'livingValue'}, true);
        //$this->livingAdvice = json_decode($data->{'livingAdvice'}, true);
    }

    function getLocation() {
        echo $this->location;
    }

    function getDate() {
        echo $this->date;
    }

    function getWarning() {
        echo $this->warning;
    }

    function getAqi() {
        echo $this->aqi;
    }

    function getMaxTemp() {
        echo $this->maxTemp;
    }

    function getMinTemp() {
        echo $this->minTemp;
    }

    function getWeather() {
        echo $this->weather.$this->icon;
    }

    function getImgPath() {
        echo $this->imgPath;
    }

    function getWind() {
        echo $this->wind;
    }

    function getLivingIndex() {
        echo $this->livingIndex;
    }

    function getLivingValue() {
        echo $this->livingValue;
    }

    function getLivingAdvice() {
        echo $this->livingAdvice;
    }
}

if (isset($parameter) && $parameter != "") {
    $dataObj->setData($parameter);
} else {
    $dataObj->setData("{\"location\":\"上海\",\"date\":\"7/13\",\"warning\":\"高温预警\",\"minTemp\":21,\"maxTemp\":30,\"weather\":4,\"wind\":\"南风微风\",\"livingIndex\":[\"紫外线\",\"紫外线\",\"紫外线\"],\"livingValue\":[\"三级\",\"三级\",\"三级\"],\"livingAdvice\":[\"注意防晒\",\"注意防晒\",\"注意防晒\"],\"aqi\":\"优\"}");
}