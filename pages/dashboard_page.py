from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage(BasePage):
        # TIMEOUT =10
        def switch_to_tab(self,tab="transaction"):    
            t = self.TIMEOUT
            self.click((By.CSS_SELECTOR, f".tabs .tab[data-tab='{tab}']"),t)


        def to_transfer_page(self):
            t = self.TIMEOUT
            driver=self.driver
            original_window_handle = driver.current_window_handle
            tab_element=self.find((By.CSS_SELECTOR,".tabs .tab[data-tab='transfer']"),t)
            # tab_element  = driver.find_element(By.CSS_SELECTOR,".tabs .tab[data-tab='transfer']")
            # switch_tab(driver,tab)
            ActionChains(driver).context_click(tab_element).perform()
            self.click((By.CLASS_NAME,"ctx-item"),t)
            WebDriverWait(driver,t).until(EC.number_of_windows_to_be(2))
            new_window_handle = (set(driver.window_handles) - {original_window_handle}).pop()
            driver.switch_to.window(new_window_handle)
            assert driver.current_window_handle == new_window_handle
            print(driver.current_url)
            self.wait_url_contains("transfer_page",timeout=10)
            # wait.until(EC.any_of(
            #     EC.element_to_be_clickable((By.NAME,"toAccountNo")),
            #     EC.text_to_be_present_in_element((By.ID,"transferNotOpened"),f"账户已冻结，无法转账")
            


        def back_dashboard_from_transfer(self):
                t = self.TIMEOUT
                self.click((By.CSS_SELECTOR,".user-area a.btn-sm"),t)
                self.wait_url_contains("dashboard",timeout=10)
                self.wait_text_contains((By.CSS_SELECTOR,".user-area button.btn-sm"),"退出")



