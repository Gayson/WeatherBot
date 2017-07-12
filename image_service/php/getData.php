<?php
$method = $argv[1];
$parameter = $argv[2];
$dataObj = new Data;

class Data {
    private $city, $date, $maxTemp, $minTemp, $weather, $wind;
    private $livingIndex, $livingValue, $livingAdvice;

    public function setData($jsonData) {
        $data = json_decode($jsonData);
        $this->city = $data->{'city'};
        $this->date = $data->{'date'};
        $this->maxTemp = $data->{'maxTemp'};
        $this->minTemp = $data->{'minTemp'};
        $this->weather = $data->{'weather'};
        $this->wind = $data->{'wind'};
        $this->livingIndex = json_decode($data->{'livingIndex'}, true);
        $this->livingValue = json_decode($data->{'livingValue'}, true);
        $this->livingAdvice = json_decode($data->{'livingAdvice'}, true);
    }

    public function getCity() {
        return $this->city;
    }

    public function getDate() {
        return $this->date;
    }

    public function getMaxTemp() {
        return $this->maxTemp;
    }

    public function getMinTemp() {
        return $this->minTemp;
    }

    public function getWeather() {
        return $this->weather;
    }

    public function getWind() {
        return $this->wind;
    }

    public function getLivingIndex() {
        return $this->livingIndex;
    }

    public function getLivingValue() {
        return $this->livingValue;
    }

    public function getLivingAdvice() {
        return $this->livingAdvice;
    }
}

if (isset($method) && $method != "" && isset($parameter) && $parameter != "") {
    $dataObj->$method($parameter);
} else {
    echo "Function call error";
}