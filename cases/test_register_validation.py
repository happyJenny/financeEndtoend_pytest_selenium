
import pytest

# from  util.util import to_login_register_page,regist,login,switch_tab,open_account
from data.user_factory import Users_Factory

from pages.home_page import HomePage
from pages.register_page import RegisterPage
VALID_IDCARD =  "dd1111222111111111"   
VALID_PHONE  = "2d800138000"
# @pytest.mark.skip
@pytest.mark.smoke     
def test_register_ok(driver_conftest):
        driver= driver_conftest
        hp=HomePage(driver)
        
        hp.to_login_register_page("register", "注册")
        register_Page=RegisterPage(driver)

        registerData = Users_Factory.build()
        print(registerData)
        register_Page.register(**registerData)
        ok=register_Page.register_ok()
        assert ok, f"failed msg is {register_Page.register_fail_msg()}"

@pytest.mark.validation   
@pytest.mark.parametrize("username,password,realname,idCard,phone,msg",
[
    ("","jepeng","ui-test","111111222111111111",VALID_PHONE,"请填写此字段。"),   
    ("uiuiuiui---","","ui-test","111111222111111111",VALID_PHONE,"请填写此字段。"),   
   ("uiuiuiui---","jepeng","","111111222111111111",VALID_PHONE,"请填写此字段。"),   
      ("uiuiuiui---","jepeng","ui","",VALID_PHONE,"请填写此字段。"),   
         ("uiuiuiui---","jepeng","test","111111222111111111","","请填写此字段。"),   
    ("alice","jepeng","ui-test",VALID_IDCARD,"1434324234","手机号必须为 11 位"), 
    ("aliceandbob","jepeng","ui-test","234",VALID_PHONE,"身份证号必须为 18 位"),
    ("alice","jepeng","ui-test",VALID_IDCARD,VALID_PHONE,"用户名已存在"),  
    ("alicehhandaron","jepeng","ui-test",VALID_IDCARD,"18514124d5e","手机号已注册"),   
    ("alicehhandaron","jepeng","ui-test","89dddddddddddddddd",VALID_PHONE,"身份证已注册"),  
#     ("' OR '2'='2","jepeng","ui-test",VALID_IDCARD,VALID_PHONE,"SQL注入"),  
])
def test_register_validation(driver_conftest,username,password,realname,idCard,phone,msg):
        driver= driver_conftest
        hp=HomePage(driver)
        
        hp.to_login_register_page("register", "注册")
        register_Page=RegisterPage(driver)

        register_Page.register(username,password,realname,idCard,phone)
        invalid=register_Page.get_first_invalid_msg()
        # print(invalid)
        if invalid:
           actual_msg=invalid
        #    print(f"some{actual_msg}")
           assert msg in actual_msg,f"原始html actual_msg is {actual_msg}, expected msg is {msg}"     
        else:
            actual_msg=register_Page.register_fail_msg()
        #    print(f"regist_fail_{actual_msg}")
            assert msg in actual_msg, f"后端 actual_msg is {actual_msg}, expected msg is {msg}"
