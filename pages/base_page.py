from selenium.common.exceptions import TimeoutException
from selenium import webdriver


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
class BasePage:
    TIMEOUT =5
    def __init__(self,driver,base_url="http://localhost:8080/"):
        self.driver=driver
        self.base_url=base_url

    def goto(self,path=""):
            return self.driver.get(self.base_url+path)

    def current_url(self):
         return self.driver.current_url    

    def _wait(self,timeout=None):
         return WebDriverWait(self.driver,timeout=timeout or self.TIMEOUT)

    def find(self,locator,timeout=None):
        return self._wait(timeout=timeout).until(
            EC.presence_of_element_located(locator))

    def find_visible(self,locator,timeout=None):
        return self._wait(timeout=timeout).until(
                EC.visibility_of_element_located(locator))

    def is_visible(self,locator,timeout=None):
        try: 
            self._wait(timeout=timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False              

    def is_absent_or_invisible(self,locator,timeout=None):
        try: 
            self._wait(timeout=timeout).until(
                EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False      

    def text_of_visible(self,locator,timeout=None):
        return self.find_visible(locator,timeout=timeout).text



    def click(self,locator,timeout=None):
        self._wait(timeout=timeout).until(
            EC.element_to_be_clickable(locator)).click()

    def fill(self,locator,text,timeout=None):
        ele=self.find_visible(locator,timeout=timeout)
        ele.clear()
        ele.send_keys(text)

    def wait_url_contains(self,url,timeout=None):
          self._wait(timeout=timeout).until(
            EC.url_contains(url))

    def wait_title_contains(self,title,timeout=None):
          self._wait(timeout=timeout).until(
            EC.title_contains(title))        

    def is_text_contains(self,locator,text,timeout=None):
        try: 
            self._wait(timeout=timeout).until(
                EC.text_to_be_present_in_element(locator,text))           
            return True
        except TimeoutException:
            return False         


    def wait_text_contains(self, locator, text, timeout=None):   # 原语义：超时抛异常
        return self._wait(timeout=timeout).until(
        EC.text_to_be_present_in_element(locator, text))   

    def get_first_invalid_msg(self):
            """
            获取表单中第一个未通过 HTML5 校验的输入框的错误信息。
            如果全部通过，返回空字符串。
            """
                            # let form = document.getElementById('registerForm'); // 假设你的表单id是这个
            # 使用 JavaScript 直接查询表单中所有的 input，并找出第一个 :invalid 的元素
            script = """

                let invalidInput = document.querySelector('input:invalid');
                return invalidInput ? invalidInput.validationMessage : '';
            """
            return self.driver.execute_script(script)               