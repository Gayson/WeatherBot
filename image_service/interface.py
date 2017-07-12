from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get('http://localhost:8080/index.php')
driver.save_screenshot("2.png")
driver.close()
