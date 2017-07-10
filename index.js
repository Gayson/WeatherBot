$(document).ready(function () {
    $('.city').text('上海天气');
    $('.date').text('07-10');
    $('.maxTemp').text('30');
    $('.minTemp').text('21');
    $('.weather').text('多云');
    $('.wind').text('南风微风');

    
});


function generateImage() {
    return html2canvas($('.img')).then(function(canvas) {
        var url = canvas.toDataURL();
        return url;
    });
}

function getData(jsonData) {
    var data;
    try {
        data = JSON.parse(jsonData);
    } catch (e) {
        console.log(e);
    }
    $('.city').text(data.city);
    $('.date').text(data.date);
    $('.maxTemp').text(data.maxTemp);
    $('.minTemp').text(data.minTemp);
    $('.weather').text(data.weather);
    $('.wind').text(data.wind);
}