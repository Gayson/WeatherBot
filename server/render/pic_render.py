# coding=utf-8
import execjs

# test json
json_info = '{"result": {"livingAdvice": ["减少室外活动", "及时调整心情", "根据温度调整"], "aqi": 91.22222222222223, "weather": "13", "livingValue": ["较差", "差", "炎热"], "quality": "AirType.MODERATE", "livingIndex": ["污染扩散", "心情", "穿衣"], "maxTemp": 37, "minTemp": 31, "warning": "高温黄色预警", "location": "上海", "wind": "南"}}'


class PicRender(object):
    def __init__(self, file_name):
        file_content = self.get_js_content(file_name)
        self.pic_ctx = execjs.compile(file_content)

    @staticmethod
    def get_js_content(file_name):
        f = open(file_name, 'r')
        file_content = f.read()
        return file_content


if __name__ == '__main__':
    # service = WeatherService()
    # service.refresh()
    # service.refresh_total_info()

    pic_render = PicRender('./../../generateImage/js/index.js')
    pic_render.pic_ctx.call('getData', json_info)
