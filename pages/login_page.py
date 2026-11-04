from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from assertions.assertions import LoginError

class LoginPage(BasePage):
        # TIMEOUT =10


        def login(self,username,password):
            self.fill((By.NAME,"username"),username)
            self.fill((By.NAME,"password"),password)
            self.click((By.CSS_SELECTOR,"button[type='submit']"))

            try:
                    self.wait_url_contains("dashboard")
                    return  None
            except TimeoutException:
                    pass    

            try:
                    error=self.text_of_visible((By.CSS_SELECTOR,".msg.msg-error"),timeout=self.SHORT_TIMEOUT)
                    raise(LoginError(error,current_url=self.driver.current_url))
            except TimeoutException:
                    front_error=self.get_first_invalid_msg()      
                    raise(LoginError(front_error,current_url=self.driver.current_url))





