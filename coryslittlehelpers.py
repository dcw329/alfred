from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import random
import requests
from bs4 import BeautifulSoup
from lxml import html
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def phrase():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87")
    driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.set_window_size(1440, 900)
    driver.maximize_window()
    url = "http://www.fiftyshadesgenerator.com/"
    driver.get(url)
    sexy = driver.find_element_by_id('text').text
    sexy = sexy.split('.')
    num = len(sexy)
    item = random.randrange(0, num)
    time.sleep(2)
    return sexy[item].strip('.')
    driver.close()


def kickuser(human_nick):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87")
    driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.set_window_size(1440, 900)
    driver.maximize_window()
    driver.get("http://blue.corypulm.com:9090/login.jsp?url=%2Fmuc-room-occupants.jsp%3FroomJID%3Dderp%2540conference.blue.corypulm.com%26nickName%3D" + human_nick + "%26kick%3D1")
    driver.find_element_by_id("u01").clear()
    driver.find_element_by_id("u01").send_keys("admin")
    driver.find_element_by_id("p01").clear()
    driver.find_element_by_id("p01").send_keys("VUgVv6VexUnuoHCrzxOM")
    driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    driver.close()


def pickup(human_nick):
    headers = {'User-Agent': 'Pewbot v1.1 by Cory Pulm - Please dont hate me <3', 'From': 'corypulm@gmail.com'}
    page = requests.get('http://www.pickuplinegenerator.com/', headers=headers)
    soup = BeautifulSoup(page.text)
    pickup = str(soup.select('h2')).split('>')
    pickup = str(pickup[1])
    pickup = pickup.split('<')
    return pickup[0]

def insult():
    headers = {'User-Agent': 'Pewbot V1.0 by Cory Pulm - Hope you dont mind me using your site <3', 'From': 'corypulm@gmail.com'}
    r = requests.get("http://www.insultgenerator.org/", headers=headers)
    tree = html.fromstring(r.text)
    insult = tree.xpath('//div[@class="wrap"]/text()')
    return insult
