from selenium import webdriver



def chrome_driver(headless: bool = False):
        option=webdriver.ChromeOptions()
        option.add_argument("--window-size=800,1000")
        if headless:
                option.add_argument("--headless=new")          # Chrome 109+ 用 new，老版本用 --headless
                option.add_argument("--disable-gpu")           # Windows 老驱动兜底
                option.add_argument("--no-sandbox")  
        Service=webdriver.ChromeService(executable_path=r"D:\tools\chromdrivers\chromedriver-win64\chromedriver.exe")
        driver=webdriver.Chrome(service=Service,options=option)
  
        return driver