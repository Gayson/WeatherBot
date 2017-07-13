# coding=utf-8
from selenium import webdriver
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ImageService(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def generate_image(self, image_data, path, callfunc):
        image_data = image_data.encode('utf-8')

        file_object = open('data.txt', 'w+')
        file_object.write(image_data)
        file_object.close()

        self.driver.get('http://localhost:8080/index.php?data=' + image_data)
        self.driver.save_screenshot(path)

        callfunc()

    def __del__(self):
        self.driver.close()

