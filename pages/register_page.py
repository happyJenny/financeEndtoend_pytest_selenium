from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from assertions.assertions import RegisterError

class RegisterPage(BasePage):
        # TIMEOUT =10


        def register(self,username,password,realName,idCard,phone):
            # t = self.TIMEOUT
            self.fill((By.NAME,"username"),username)
            self.fill((By.NAME,"password"),password)
            self.fill((By.NAME,"realName"),realName)
            self.fill((By.NAME,"phone"),phone)
            self.fill((By.NAME,"idCard"),idCard)
            self.click((By.CSS_SELECTOR,"button[type='submit']"))

            try:
                self.wait_url_contains("login")
                return None
            except TimeoutException:    
                pass

            try:
                error=self.text_of_visible((By.CSS_SELECTOR,".msg.msg-error"),timeout=self.SHORT_TIMEOUT)
                raise RegisterError(error,current_url=self.driver.current_url)
            except TimeoutException:    
                error=self.get_first_invalid_msg()
                raise RegisterError(error,current_url=self.driver.current_url)    


 