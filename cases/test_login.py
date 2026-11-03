
import pytest

# from  util.util import to_login_register_page,regist,login,switch_tab,open_account
from data.user_factory import Users_Factory

from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
VALID_IDCARD =  "dd1111222111111111"   
VALID_PHONE  = "2d800138000"
# @pytest.mark.skip
@pytest.mark.smoke
def test_login_ok(driver_conftest):
        driver= driver_conftest
        hp=HomePage(driver)
        
        hp.to_login_register_page("login", "登录")
        login_Page=LoginPage(driver)
        login_Page.login("alice","jepeng")
        ok=login_Page.loign_ok()


        assert ok, f"failed msg is {login_Page.login_fail_msg()}"

@pytest.mark.validation        
@pytest.mark.parametrize("username,password,msg",
[
  ("jepeng","","请填写此字段"),
  ("","jepeng","请填写此字段"),
  ("alice","je","用户名或密码错误"),
])
def test_login_validation(driver_conftest,username,password,msg):
        driver= driver_conftest
        hp=HomePage(driver)
        
        hp.to_login_register_page("login", "登录")
        login_Page=LoginPage(driver)
        login_Page.login(username,password)
        invalid=login_Page.get_first_invalid_msg()
        # print(invalid)
        if invalid:
           actual_msg=invalid
           assert msg in actual_msg, f"原始html actual_msg is {actual_msg}, expected msg is {msg}"    

        else:
           actual_msg=login_Page.login_fail_msg()
           assert msg in actual_msg, f"后端 actual_msg is {actual_msg}, expected msg is {msg}"
  
