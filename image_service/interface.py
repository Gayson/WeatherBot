# coding=utf-8
import PIL.Image
from selenium import webdriver
import sys
from server import utils

reload(sys)
sys.setdefaultencoding('utf-8')


class ImageService(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def generate_image(self, image_data, path, callfunc):
        image_data = image_data.encode('utf-8')

        file_object = open(utils.get_data_file_path(), 'w+')
        file_object.write(image_data)
        file_object.close()

        self.driver.get('http://localhost:8080/index.php')
        element = self.driver.find_element_by_class_name('img')
        self.driver.save_screenshot(path)

        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        im = PIL.Image.open(path)
        im = im.crop((left, top, right, bottom))
        im.save(path)

        callfunc()

    def __del__(self):
        self.driver.close()

