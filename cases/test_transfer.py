
import pytest
import re

# from  util.util import to_login_register_page,regist,login,switch_tab,open_account
from data.user_factory import Users_Factory

from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.transfer_page import TransferPage
from assertions.assertions import TransferError
VALID_IDCARD =  "dd1111222111111111"   
VALID_PHONE  = "2d800138000"
# @pytest.mark.skip

FROZEN_USER = "UI_test_0166dbff"
NORMAL_USER = "alice"

def _login_and_open_transfer(driver,username,password):

        hp=HomePage(driver)  
        hp.to_login_register_page("login", "登录")
        login_Page=LoginPage(driver)
        login_Page.login(username,password)
        ok=login_Page.loign_ok()


        assert ok, f"failed msg is {login_Page.login_fail_msg()}"
        dashboard_page=DashboardPage(driver)
        dashboard_page.to_transfer_page()
        transfer_page=TransferPage(driver)
        return  dashboard_page,transfer_page


@pytest.mark.smoke
def test_transfer_from_frozen(driver_conftest): 

        dashboard_page,transfer_page= _login_and_open_transfer(driver_conftest,FROZEN_USER,"jepeng")
        ok=transfer_page.is_frozen()
        assert ok, "this should be show the freeze info" 

@pytest.mark.smoke
def test_transfer_valid(driver_conftest):

        dashboard_page,transfer_page= _login_and_open_transfer(driver_conftest,NORMAL_USER,"jepeng")
        assert transfer_page.is_form_ready(),"didn't find the account input"


        old_balance=transfer_page.myBalance()
        amount=11
        transfer_page.transfer("6436265847",amount)
        # assert transfer_page.transfer_ok(amount), f"转账成功，amount{amount}"
        new_balance=transfer_page.myBalance()
        assert round(new_balance*100)==round(old_balance*100)-round(amount*100)
        dashboard_page.back_dashboard_from_transfer()


@pytest.mark.validation  
@pytest.mark.parametrize("accountNum,amount,msg",
[
  ("6436265847","","请填写此字段"),
  ("","11","请填写此字段"),
  ("6436265847","-1","值必须大于或等于 0.01"),
    ("6436","11","转入账户不存在"),
#    ("6436","11","账号不存在"),
])
def test_transfer_invalid(driver_conftest,accountNum,amount,msg):

        dashboard_page,transfer_page= _login_and_open_transfer(driver_conftest,"alice","jepeng")
        old_balance=transfer_page.myBalance()
        

        with pytest.raises(TransferError,match=re.escape(msg)):
                transfer_page.transfer(accountNum,amount)


        new_balance=transfer_page.myBalance()   
        assert round(new_balance*100)==round(old_balance*100)


