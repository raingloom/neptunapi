from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, WebDriverException
from urllib.parse import urljoin
import code

import neptun.constants as nconst

NeptunURL="https://hallgato.neptun.elte.hu"

class UnexpectedPageStateException(WebDriverException):
    pass

class Client:
    def __init__(self,browser):
        self.browser=browser
    def logout(self):
        browser=self.browser
        try:
            elogout=browser.find_element_by_id("lbtnQuit")
            elogout.click()
        except NoSuchElementException as e:
            try:
                browser.execute_script("DoLogOut(-1)")#this is what the UI calls internally
            except Exception as e:
                raise UnexpectedPageStateException("could not find suitable logout method") from e
    def login(self,name,passw,bypass=True):
        browser=self.browser
        browser.get(urljoin(NeptunURL,"login.aspx"))
        user=browser.find_element_by_id("user")
        pwd=browser.find_element_by_id("pwd")
        user.clear()
        user.send_keys(name)
        pwd.clear()
        pwd.send_keys(passw)
        try:
            pwd.send_keys("\n")
            WebDriverWait(browser,10).until(expected_conditions.staleness_of(user),"Login page timed out. Did you enter the correct credentials?")
        except UnexpectedAlertPresentException as e:
            if bypass:
                Alert(browser).accept()
                self.login(name,passw,bypass=False)
            else:
                raise UnexpectedPageStateException("Unexpected alert. Pass bypass=True to Client.login() to avoid it.") from e
    def is_logged_in(self):
        browser=self.browser
        browser.get(urljoin(NeptunURL,"main.aspx"))
        try:
            browser.find_element_by_id(nconst.logout)
        except NoSuchElementException:
            return False
        finally:
            return True
    def skip_messages(self):
        browser=self.browser
        while True:
            try:
                browser.find_element_by_id(nconst.nextmsg)
            except:
                #element no longer present
                break
    def kill_logout_timer(self):
        self.browser.execute_script("clearTimeout(timerID2)")
    def maxout_logout_timer(self):
        self.browser.execute_script("countdown=~(1<<63)")
        
        
        
