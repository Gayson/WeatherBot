var $ = require('jquery');
var html2canvas = require('html2canvas');
var codeToWeather = require('./code2Weather.js');

function generateImage(location) {
    return html2canvas($('.img')).then(function (canvas) {
        var base64 = canvas.toDataURL();
        $.ajax({
            type: "POST",
            url: "./php/saveImg.php",
            data: {
                base64: base64,
                location: location
            },
            dataType: "json",
            success: function () {
                console.log('transmit image success');
            }
        });
        return base64;
    });
}

function getData(jsonData) {
    var data;
    try {
        data = JSON.parse(jsonData);
    } catch (e) {
        console.log(e);
    }

    $('.location').text(data.location);
    $('.date').text(data.date);
    $('.maxTemp').text(data.maxTemp);
    $('.minTemp').text(data.minTemp);
    $('.wind').text(data.wind);
    $('.aqi').text(data.aqi);

    codeToWeather(data.weather);

    if (data.warning === '') {
        $('.warning').hide();
    }
    else {
        $('.warning').text(data.warning);
    }

    $('.living').each(function (index) {
        var livingIndex = "<span class='livingIndex'>" + data.livingIndex[index] + "</span>";
        var livingValue = "<span class='livingValue'>" + data.livingValue[index] + "</span>";
        var livingAdvice = "<span class='livingAdvice'>" + data.livingAdvice[index] + "</span>";
        $('.living:eq(' + index + ')').append(livingIndex).append(livingValue).append(livingAdvice);
    })
    console.log(111);
    generateImage(data.location);
}

function generateTestData() {
    var json = {};
    var date = new Date();
    var month = date.getMonth() + 1;
    var day = date.getDate();

    json.location = '上海';
    json.date = month + "/" + day;
    json.warning = '高温预警';
    json.minTemp = 21;
    json.maxTemp = 30;
    json.weather = 4;
    json.wind = '南风微风';
    json.livingIndex = ['紫外线', '紫外线', '紫外线'];
    json.livingValue = ['三级', '三级', '三级'];
    json.livingAdvice = ['注意防晒', '注意防晒', '注意防晒'];
    json.aqi = '优';
    return json;
}