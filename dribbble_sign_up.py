import random

from selenium import webdriver
import proxy_lister

# proxy = proxy_lister.Proxy()
# proxy.scrapForLiveProxy()
with open('proxy_list.txt') as file:
    ip_list = file.read().split('\n')
    file.close()


def sign_up(fullname, username, password, emailid):

    ip_port = str(random.choice(ip_list))
    ip_port = ip_port.split(' ')
    ip = ip_port[0]
    port = ip_port[1]
    PROXY = "{}:{}".format(ip, port)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
    driver.get('https:dribbble.com/signup/new')

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
    if input('Enter \'v\': '):
        print("Closing driver...")
        driver.close()


with open('credentials.txt', 'r') as file:
    credentials = file.read().split('\n')
    file.close()

with open('filled_up_dribbble.txt', 'r+') as file:
    filled_cred = file.read().split('\n')
    file.close()
count = 0
while count < 150:
    credential = credentials[count].split(' ')
    if credential[2] not in filled_cred:
        fullname = credential[0] + ' ' + credential[1]
        emailid = credential[2] + '@yandax.com'
        username = credential[2]
        password = credential[3]
        sign_up(fullname, username, password, emailid)
        with open('filled_up_dribbble.txt', 'a+') as file:
            file.write('\n')
            file.write(credential[2])
            file.close()
        count += 1
    else:
        count += 1
        continue
    print("Current user: ", count)
