# coding=utf-8
from selenium import webdriver
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ImageService(object):
    def __init__(self, image_data):
        image_data = image_data.encode('utf-8')

        file_object = open('test.txt', 'w+')
        file_object.write(image_data)
        file_object.close()

        driver = webdriver.PhantomJS()
        driver.get('http://localhost:8080/index.php')
        path = unicode("上海0713.png", "utf8")
        driver.save_screenshot(path)
        driver.close()


if __name__ == '__main__':
    img = ImageService("{\"result\": {\"livingIndex\": [\"污染扩散\", \"心情\", \"穿衣\"], \"maxTemp\": 36, \"livingAdvice\": [\"减少室外活动\", \"及时调整心情\", \"根据温度调整\"], \"aqi\": 82.44444444444444, \"minTemp\": 31, \"warning\": \"高温橙色预警\", \"livingValue\": [\"中\", \"较差\", \"炎热\"], \"weather\": \"4\", \"location\": \"上海\", \"date\": \"2017-07-13\", \"quality\": \"1\", \"wind\": \"南\", \"details\": [\"气象条件对空气污染物稀释、扩散和清除无明显影响，易感人群应适当减少室外活动时间。\", \"天气较好，气温较高，会让人觉得有些烦躁，注意室内通风降温，保持心态平和，给自己的情绪“降降温”。\", \"天气炎热，建议着短衫、短裙、短裤、薄型T恤衫等清凉夏季服装。\"]}}")



