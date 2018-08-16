import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time


def openDriver():

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("incognito")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://passport.yandex.com/registration/mail?from=mail&require_hint=1&origin=hostroot_homer_reg_v3_com&retpath=https%3A%2F%2Fmail.yandex.com%2F&backpath=https%3A%2F%2Fmail.yandex.com%3Fnoretpath%3D1')

    # Filling up the details
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[3]/div/div[2]/span').click()
    firstNameField = driver.find_element_by_xpath('//*[@id="firstname"]')
    lastNameField = driver.find_element_by_xpath('//*[@id="lastname"]')
    usernameField = driver.find_element_by_xpath('//*[@id="login"]')
    passwordField = driver.find_element_by_xpath('//*[@id="password"]')
    reEnterPasswordField = driver.find_element_by_xpath('//*[@id="password_confirm"]')
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[3]/div[1]/div/div[1]/span[1]/span/button').click()
    i = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    query = '/html/body/div[2]/div/div/div[' + str(i) + ']/span'
    driver.find_element_by_xpath(query).click()
    answerField = driver.find_element_by_xpath('//*[@id="hint_answer"]')
    answer = ""
    for i in range(15):
        answer += random.choice(list("qwertyuiopasdfghjkzxcvbnm    "))
    firstNameField.send_keys(content[0])
    lastNameField.send_keys(content[1])
    usernameField.send_keys(content[2])
    passwordField.send_keys(content[3])
    reEnterPasswordField.send_keys(content[3])
    answerField.send_keys(answer)
    if input('Enter \'v\': ') == 'v':
        driver.close()


with open('credentials.txt', 'r') as file:
    contents = file.read()
    contents = contents.split('\n')
    file.close()
final_cred = []
for content in contents:
    content = content.split(' ')
    final_cred.append(content)
count = 0
already_filled = []

with open('filled_up.txt', 'r+') as file:
    try:
        added = file.read()
        already_filled = added.split('\n')
    except Exception as e:
        print("Some error faced while reading the file 'filled_up.txt'", e)
while count < 150:
    content = final_cred[count]
    if content[2] not in already_filled:
        openDriver()
        with open('filled_up.txt', 'a+') as file:
            file.write('\n')
            file.write(content[2])
            file.close()
        count += 1
    else:
        count += 1
        continue
    print("Current user: ", count)


