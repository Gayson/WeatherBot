$(document).ready(function () {
    $('.city').text('上海天气');
    $('.date').text('07-10');
    $('.maxTemp').text('30');
    $('.minTemp').text('21');
    $('.weather').text('多云');
    $('.wind').text('南风微风');
    alert(generateImage());
})


function generateImage() {
    html2canvas($('.img')).then(function(canvas) {
        var url = canvas.toDataURL();
        return url;
    });
}