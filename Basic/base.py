from selenium.webdriver.support.wait import WebDriverWait

class Base(object):
    def __init__(self,driver):
        self.driver  = driver
    def find_element(self,loc,timeout=10):
        # 封装为智能等待方法
        # loc:类型为元组，格式（By.ID,value),(By.CLASS_NAME,value),(By.XPATH,value)
        # timeout : 搜索超时时间
         return WebDriverWait(self.driver,timeout).until(lambda x: x.find_element(*loc))

    def click_element(self,loc):
        self.find_element(loc).click()
