from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class RegisterPage(BasePage):
        # TIMEOUT =10


        def register(self,username,password,realName,idCard,phone):
            t = self.TIMEOUT
            self.fill((By.NAME,"username"),username,t)
            self.fill((By.NAME,"password"),password,t)
            self.fill((By.NAME,"realName"),realName,t)
            self.fill((By.NAME,"phone"),phone,t)
            self.fill((By.NAME,"idCard"),idCard,t)
            self.click((By.CSS_SELECTOR,"button[type='submit']"),t)


        def register_ok(self):     
            try:
                self.wait_url_contains("login",timeout=10)
                return  True
            except TimeoutException:
                return False    

        def register_fail_msg(self):
                # print(self.current_url())
            # if "login" not in self.current_url():
                return self.text_of_visible((By.CSS_SELECTOR,".msg.msg-error"),timeout=self.TIMEOUT)
                # raise AssertionError(f"注册失败: {err} (url={self.current_url()})")

        # def register_blank_msg(self,blank,msg="请填写此字段"):     
        #          return self.find_visible((By.CSS_SELECTOR,f"input[name='{blank}']")).text   

        # def get_first_invalid_msg(self):
        #     """
        #     获取表单中第一个未通过 HTML5 校验的输入框的错误信息。
        #     如果全部通过，返回空字符串。
        #     """
        #                     # let form = document.getElementById('registerForm'); // 假设你的表单id是这个
        #     # 使用 JavaScript 直接查询表单中所有的 input，并找出第一个 :invalid 的元素
        #     script = """

        #         let invalidInput = document.querySelector('input:invalid');
        #         return invalidInput ? invalidInput.validationMessage : '';
        #     """
        #     return self.driver.execute_script(script)         



  