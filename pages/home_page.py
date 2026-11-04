from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
class HomePage(BasePage):
        # TIMEOUT =10



        def to_login_register_page(self,page_name,title): 
            # print(page_name,title,timeout)
            self.goto()
            self.wait_title_contains("Finance")
            self.click((By.CSS_SELECTOR,f"[href='/{page_name}.html']"))
            self.wait_title_contains(title)    

