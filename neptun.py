from selenium.webdriver.remote.webdriver import WebDriver
from waiter import is_stale
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
class Client:
    def __init__(self,browser):
        self.browser=browser
    def login(self,name,passw):
        browser=self.browser
        browser.get("https://hallgato.neptun.elte.hu/login.aspx")
        user=browser.find_element_by_id("user")
        pwd=browser.find_element_by_id("pwd")
        user.clear()
        user.send_keys(name)
        pwd.clear()
        pwd.send_keys(passw)
        WebDriverWait(browser,10).until(expected_conditions.staleness_of(user),"Login page timed out. Did you enter the correct credentials?")