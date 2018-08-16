from selenium import webdriver


class Proxy:
    def __init__(self):
        print("Scrapping for live proxies...")

    @staticmethod
    def scrapForLiveProxy():
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://free-proxy-list.net/')
        search = driver.find_element_by_xpath('//*[@id="proxylisttable_filter"]/label/input')
        search.send_keys('India')
        # with open('proxy_list.txt', 'w+') as file:
        i = 1
        lists = []
        while True:
            try:
                path_ip = '//*[@id="proxylisttable"]/tbody/tr[' + str(i) + ']/td[1]'
                ip = driver.find_element_by_xpath(path_ip).text
                path_port = '//*[@id="proxylisttable"]/tbody/tr[' + str(i) + ']/td[2]'
                port = driver.find_element_by_xpath(path_port).text
                lists.append([ip, port])
                i += 1
            except Exception as e:
                print("Ran into error", e)
                break
        with open('proxy_list.txt', 'w+') as file:
            for content in lists:
                ip_port = '\n' + content[0] + ' ' + content[1]
                file.write(ip_port)
            file.close()
        driver.close()
