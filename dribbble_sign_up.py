import random

from selenium import webdriver
import proxy_lister
from selenium.webdriver.common.proxy import *

proxy = proxy_lister.Proxy()
proxy.scrapForLiveProxy()
with open('proxy_list.txt') as file:
    ip_list = file.read().split('\n')
    file.close()


def sign_up(fullname, username, password, emailid):

    ip_port = str(random.choice(ip_list))
    ip_port = ip_port.split(' ')
    ip = ip_port[0]
    port = ip_port[1]

    # options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument("--test-type")
    # options.add_argument('--proxy-server=%s' % PROXY)
    # driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
    # driver.get('https:dribbble.com/signup/new')

    driver = webdriver.Firefox()
    profile = webdriver.FirefoxProfile('/home/fake_batman/.mozilla/firefox/8n4a3ph8.default')
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", ip)
    profile.set_preference("network.proxy.http_port", port)
    profile.set_preference("network.proxy.ssl", ip)
    profile.set_preference("network.proxy.ssl_port", port)
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get('https://dribbble.com/signup/new')

    if len(username) >= 20:
        username = username[:20]
    fullnameField = driver.find_element_by_xpath('//*[@id="user_name"]')
    usrnameField = driver.find_element_by_xpath('//*[@id="user_login"]')
    passwordField = driver.find_element_by_xpath('//*[@id="user_password"]')
    emailField = driver.find_element_by_xpath('//*[@id="user_email"]')

    fullnameField.send_keys(fullname)
    usrnameField.send_keys(username)
    passwordField.send_keys(password)
    emailField.send_keys(emailid)
    input("Press enter: ")
    driver.find_element_by_xpath('//*[@id="user_location"]').send_keys(random.choice(["Mumbai", "Delhi", "Kolkata", "Bangalore", "Chennai", "Vellore", "Munsa", "vaskc"]))
    input('Enter something: ')
    print("Closing driver...")


with open('credentials.txt', 'r') as file:
    credentials = file.read().split('\n')

with open('filled_up_dribbble.txt', 'r+') as file:
    filled_cred = file.read().split('\n')

count = 0
while count < 150:
    credential = credentials[count].split(' ')
    username = credential[2]
    username = username.replace('.', '_')
    if credentials not in filled_cred:
        fullname = credential[0] + ' ' + credential[1]
        emailid = credential[2] + '@yandax.com'
        password = credential[3]
        sign_up(fullname, username, password, emailid)
        with open('filled_up_dribbble.txt', 'a+') as file:
            file.write('\n')
            file.write(username)
        count += 1
    else:
        count += 1
        continue
    print("Current user: ", count)
