<?php
try {
    $dataFile = "data.txt";
    $myfile = fopen($dataFile, "r") or die("Unable to open file!");
    $parameter = fread($myfile,filesize($dataFile));
} catch (Exception $e) {
}

$dataObj = new Data;

require('util.php');

class Data {
    private $location, $date, $warning, $aqi, $aqiQuality, $maxTemp, $minTemp,
        $weather, $icon, $imgPath, $wind;
    private $livingIndex, $livingValue, $livingAdvice;

    function setData($jsonData) {
        $data = json_decode($jsonData);
        $data = $data->{'result'};

        $this->location = $data->{'location'};
        $this->date = $data->{'date'};
        $this->warning = $data->{'warning'};
        $this->aqi = (int)$data->{'aqi'};
        $this->maxTemp = $data->{'maxTemp'};
        $this->minTemp = $data->{'minTemp'};
        $this->wind = $data->{'wind'}.'风';

        code2weather($data->{'weather'}, $this->weather, $this->icon, $this->imgPath);
        code2AqiQuality($data->{'quality'}, $this->aqiQuality);
        warningComponent($data->{'warning'}, $this->warning);

        $this->livingIndex = $data->{'livingIndex'};
        $this->livingValue = $data->{'livingValue'};
        $this->livingAdvice = $data->{'livingAdvice'};
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

    function getAqiQuality() {
        echo $this->aqiQuality;
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

    function getLivingIndex($index) {
        echo $this->livingIndex[$index];
    }

    function getLivingValue($index) {
        echo $this->livingValue[$index];
    }

    function getLivingAdvice($index) {
        echo $this->livingAdvice[$index];
    }
}

if (isset($parameter) && $parameter != "") {
    $dataObj->setData($parameter);
} else {
    //$dataObj->setData("{\"result\": {\"livingIndex\": [\"污染扩散\", \"心情\", \"穿衣\"], \"maxTemp\": 33, \"livingAdvice\": [\"减少室外活动\", \"及时调整心情\", \"根据温度调整\"], \"aqi\": 73.85714285714286, \"minTemp\": 28, \"warning\": \"无预警\", \"weather\": \"4\", \"location\": \"上海\", \"quality\": \"AirType.MODERATE\", \"wind\": \"南\", \"livingValue\": [\"较差\", \"差\", \"炎热\"]}}");
}