$(document).ready(function () {

    var date = new Date();
    var month = date.getMonth() + 1;
    var day = date.getDate();

    var json = {};
    json.location = '上海';
    json.warning = '';
    json.minTemp = 21;
    json.maxTemp = 30;
    json.weather = 22;
    json.wind = '南风微风';
    json.livingIndex = ['紫外线','紫外线','紫外线'];
    json.livingValue = ['三级','三级','三级'];
    json.livingAdvice = ['注意防晒','注意防晒','注意防晒'];
    json.aqi = '优';
    getData(JSON.stringify(json));

    $('.date').text(month + "-" + day);
    //$('.weather').prepend("<i class='wi wi-cloud'></i>");
    generateImage(json.location)
});


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
    $('.maxTemp').text(data.maxTemp);
    $('.minTemp').text(data.minTemp);
    codeToWeather(data.weather);
    $('.wind').text(data.wind);
    $('.aqi').text(data.aqi);
    if (data.warning === '')
        $('.warning').hide();
    $('.living').each(function (index, element) {
        var livingIndex = "<span class='livingIndex'>" + data.livingIndex[index] + "</span>";
        var livingValue = "<span class='livingValue'>" + data.livingValue[index] + "</span>";
        var livingAdvice = "<span class='livingAdvice'>" + data.livingAdvice[index] + "</span>";
        $('.living:eq('+index+')').append(livingIndex);
        $('.living:eq('+index+')').append(livingValue);
        $('.living:eq('+index+')').append(livingAdvice);
    })
}