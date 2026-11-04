from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from assertions.assertions import TransferError 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re

class TransferPage(BasePage):
        # TIMEOUT =10

        def myBalance(self):
            raw= self.text_of_visible((By.ID,"myBalance")).strip()
            # raw = self.text_of_visible(self.BALANCE).strip()
            m = re.search(r"(-?\d[\d,]*\.?\d*)", raw)   # 抓数字（含千分位）
            if not m:
                raise AssertionError(f"未能从余额文本解析数字: {raw!r}")
            return float(m.group(1).replace(",", ""))


        # def transfer(self,toAccount,amount,remark=None):
        #     t = self.TIMEOUT
        #     if remark==None:
        #         remark=f"转账 {amount}"
        #     self.fill((By.NAME,"toAccountNo"),toAccount,t)
        #     self.fill((By.NAME,"amount"),amount,t)
        #     self.fill((By.NAME,"remark"),remark,t)
        #     self.click((By.CSS_SELECTOR,"button[type='submit']"),t)


        #     success_loc = (By.CSS_SELECTOR, ".inline-msg.success")
        #     error_loc   = (By.CSS_SELECTOR, ".inline-msg.error")

        #     try:
        #         result = self._wait(timeout=10).until(EC.any_of(
        #             EC.text_to_be_present_in_element(success_loc, f"转账成功 -¥{amount}"),
        #             EC.visibility_of_element_located(error_loc),
        #         ))
        #     except TimeoutException:
        #         invalid = self.get_first_invalid_msg()
        #         raise TransferError(
        #             invalid or "转账后 10s 内既无提示也未跳转",
        #             current_url=self.current_url())

        #     # result 只可能是 True（成功文案）或 error 的 WebElement
        #     if result is True:
        #         return None

        #     # 此时 result 就是那个 error 元素；优先用它的 .text，避免再查一次
        #     err = (result.text or "").strip()
        #     if not err:
        #         # 兜底：元素在但文本暂时为空，再读一次（仍可能空，但至少不改变"是 error"的判定）
        #         err = self.text_of_visible(error_loc, timeout=0.5)
        #     raise TransferError(err or "转账失败（未取到错误文案）",
        #                         current_url=self.current_url())



        #     # try:
        #     #     self.wait_text_contains((By.CSS_SELECTOR,".inline-msg.success"),f"转账成功 -¥{amount}",2)
        #     #     print("sss")
        #     #     return None
        #     # except TimeoutException:
        #     #     print("www")
        #     #     pass   

        #     # try:
        #     #     error=self.text_of_visible((By.CSS_SELECTOR,".inline-msg.error"),timeout=1)
        #     #     raise TransferError(error,current_url=self.driver.current_url)
        #     # except TimeoutException:    
        #     #     pass

 

        #     # try:
        #     #     error=self.text_of_visible((By.CSS_SELECTOR,".holder-info.bad"),timeout=self.TIMEOUT)
        #     #     raise TransferError(error,current_url=self.driver.current_url)   

        #     # except TimeoutException:   
        #     #     pass          

        #     # try:                
        #     #     error=self.get_first_invalid_msg()
        #     #     raise TransferError(error,current_url=self.driver.current_url)   

        #     # except TimeoutException:   
        #     #     pass  
  




        def transfer(self, toAccount, amount, remark=None):
            if remark is None:
                remark = f"转账 {amount}"
            self.fill((By.NAME, "toAccountNo"), toAccount)
            self.fill((By.NAME, "amount"), str(amount))
            self.fill((By.NAME, "remark"), remark)
            self.click((By.CSS_SELECTOR, "button[type='submit']"))

            success_loc = (By.CSS_SELECTOR, ".inline-msg.success")
            inline_err  = (By.CSS_SELECTOR, ".inline-msg.error")
            holder_loc  = (By.CSS_SELECTOR, ".holder-info.bad")

            def _txt(el):
                s = (el.text or "").strip()
                if s:
                    return s
                try:
                    return (self.driver.execute_script(
                        "return (arguments[0].textContent||arguments[0].innerText||'').trim();",
                        el) or "").strip()
                except Exception:
                    return ""

            # ── 第一段：2s 抓两个 inline，轮询 0.1s 防漏 ──
            try:
                first = self._wait_inline().until(
                    EC.any_of(
                        EC.text_to_be_present_in_element(success_loc, f"转账成功 -¥{amount}"),
                        EC.visibility_of_element_located(inline_err),
                    )
                )
            except TimeoutException:
                first = None

            if first is True:
                return None                      # success inline
            if first is not None:                # error inline → 立即读文本
                raise TransferError(_txt(first) or "转账失败（inline 无文案）",
                                    current_url=self.current_url())

            # ── 第二段：inline 没出现 → 等 holder / success ──
            try:
                result = WebDriverWait(self.driver, timeout=8).until(
                    EC.any_of(
                        EC.text_to_be_present_in_element(success_loc, f"转账成功 -¥{amount}"),
                        EC.visibility_of_element_located(holder_loc),
                    )
                )
            except TimeoutException:
                invalid = self.get_first_invalid_msg()
                raise TransferError(invalid or "转账后 10s 内既无提示也未跳转",
                                    current_url=self.current_url())

            if result is True:
                return None
            raise TransferError(_txt(result) or "转账失败（未取到错误文案）",
                                current_url=self.current_url())

        def is_form_ready(self):   
            return self.is_visible((By.NAME,"toAccountNo"))  


        def is_frozen(self):
            return self.is_text_contains((By.ID,"transferNotOpened"),f"账户已冻结，无法转账") 







  