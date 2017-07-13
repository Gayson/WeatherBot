# coding=utf-8
from selenium import webdriver
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ImageService(object):
    def __init__(self, image_data):
        self.image_data = image_data.encode('utf-8')

        print image_data
        driver = webdriver.PhantomJS()
        driver.get('http://localhost:8080/index.php?data=' + image_data)
        path = unicode("上海0713.png", "utf8")
        driver.save_screenshot(path)
        print driver.find_element_by_class_name('date').text
        driver.close()


if __name__ == '__main__':
    service = ImageService(
        "{\"result\": {\"livingIndex\": [\"污染扩散\", \"心情\", \"穿衣\"], \"maxTemp\": 35, "
        "\"livingAdvice\": [\"减少室外活动\", \"及时调整心情\", \"根据温度调整\"], \"aqi\": 73.85714285714286,"
        " \"minTemp\": 28, \"warning\": \"无预警\", \"weather\": \"4\", \"location\": \"上海\","
        " \"quality\": \"AirType.MODERATE\", \"wind\": \"南\", \"livingValue\": [\"较差\", \"差\", \"炎热\"]}}")
