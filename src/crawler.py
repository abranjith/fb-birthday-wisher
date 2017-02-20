'''
__author__ = 'Ranjith'
This script actually crawls through the website per user instructions (to post happy birthday message)
Make sure to configure Config.txt before using
'''
import ConfigParser
import os
import logging

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options

from FBPages import *

from apscheduler.schedulers.blocking import BlockingScheduler
#from datetime import datetime

def main():

    #read schedule interval data
    daily_schedule_hours = config_parser.get("SCHEDULE_SECTION", "daily_schedule_hours")

    #scheduler to run this program
    sched = BlockingScheduler()
    sched.add_job(looper, 'cron', hour=daily_schedule_hours)
    sched.start()
    #looper() #makes direct call once


def looper():

    #read parameters to enter on the website
    url = config_parser.get("BROWSER_SECTION", "url")
    username = config_parser.get("BROWSER_SECTION", "username")
    password = config_parser.get("BROWSER_SECTION", "password")
    name = config_parser.get("BROWSER_SECTION", "name_of_the_logged_in_user")
    message = config_parser.get("BROWSER_SECTION", "message")

    driver = webdriver.PhantomJS()
    '''
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36")
    opts.add_argument("disable-popup-blocking")
    driver = webdriver.Chrome(chrome_options=opts)
    '''


    try:
        driver.get(url)

        login_page = LoginPage(driver)

        login_page.login_as(username, password)
        time.sleep(5)

        if (login_page.login_is_successful(name)):
            main_page = MainPage(driver)
            main_page.goto_birthday_page()
            main_page.wish_them_all(message)
            logger.info("Operation completed successfully")
    except Exception, e:
        logger.error(e.message)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    #read and initialize from config
    config_file = os.path.join(os.path.pardir, "config", "Config.txt")
    config_parser = ConfigParser.RawConfigParser()
    config_parser.read(config_file)

    #initialize logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler(os.path.join(os.path.pardir, "log", "logger.log"))
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    main()
