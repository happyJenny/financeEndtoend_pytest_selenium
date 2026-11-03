from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import re

class TransferPage(BasePage):
        # TIMEOUT =10

        def myBalance(self):
            t = self.TIMEOUT
            raw= self.text_of_visible((By.ID,"myBalance"),t).strip()
            # raw = self.text_of_visible(self.BALANCE).strip()
            m = re.search(r"(-?\d[\d,]*\.?\d*)", raw)   # 抓数字（含千分位）
            if not m:
                raise AssertionError(f"未能从余额文本解析数字: {raw!r}")
            return float(m.group(1).replace(",", ""))


        def transfer(self,toAccount,amount,remark=None):
            t = self.TIMEOUT
            if remark==None:
                remark=f"转账 {amount}"
            self.fill((By.NAME,"toAccountNo"),toAccount,t)
            self.fill((By.NAME,"amount"),amount,t)
            self.fill((By.NAME,"remark"),remark,t)
            self.click((By.CSS_SELECTOR,"button[type='submit']"),t)

        def transfer_page_ok(self):   
            return self.is_visible((By.NAME,"toAccountNo"))  


        def transfer_page_freeze(self):
            return self.is_text_contains((By.ID,"transferNotOpened"),f"账户已冻结，无法转账") 

        def transfer_ok(self,amount):  
            t = self.TIMEOUT   
            try:
                self.wait_text_contains((By.CSS_SELECTOR,".inline-msg.success"),f"转账成功 -¥{amount}",t)

                return  True
            except TimeoutException:
                return False    


        def transfer_fail_msg(self):
                # print(self.current_url())
            # if "login" not in self.current_url():
                return self.text_of_visible((By.CSS_SELECTOR,".inline-msg.error"),timeout=self.TIMEOUT)
                # raise AssertionError(f"注册失败: {err} (url={self.current_url()})")

        # def register_blank_msg(self,blank,msg="请填写此字段"):     
        #          return self.find_visible((By.CSS_SELECTOR,f"input[name='{blank}']")).text   

        # def get_first_invalid_msg(self):
        #     """
        #     获取表单中第一个未通过 HTML5 校验的输入框的错误信息。
        #     如果全部通过，返回空字符串。
        #     """
        #     # 使用 JavaScript 直接查询表单中所有的 input，并找出第一个 :invalid 的元素
        #     script = """
        #         let invalidInput = document.querySelector('input:invalid');
        #         return invalidInput ? invalidInput.validationMessage : '';
        #     """
        #     return self.driver.execute_script(script)         



  