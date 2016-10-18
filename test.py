#!/usr/bin/env python3
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
from selenium import webdriver
import warnings
import neptun
from getpass import getpass

try:
    display = Display(visible=0, size=(1024, 768))
    display.start()
    
    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    
    #make sure we are in the correct locale
    #Hungarian seems to be the most supported
    #English even lacks some menus
    i=0
    langelem=None
    while langelem:
        try:
            langelem=browser.find_element_by_id("btn_lang%d"%i)
            title = langelem.get_attribute("title").lower()
            if "magyar" in title or "hun" in title:
                break
            langelem+=1
        except NoSuchElementException:
            pass
    if langelem:
        langelem.click()
    else:
        warnings.warn("Failed to set locale, this may cause runtime errors.",category=RuntimeWarning)
    
    nclient=neptun.Client(browser)
    if not nclient.is_logged_in():
        nclient.login(input("user:"),getpass("password:"))
    print(nclient.is_logged_in() and "is logged in" or "not logged in")
    
finally:
    print("client finished at:",browser.current_url)
    browser.save_screenshot("exit.png")
    print("saved screenshot at exit.png")
    browser.quit()
    display.stop()
    print("finalized successfully")
