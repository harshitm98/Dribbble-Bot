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
        i = 1
        lists = []
        while True:
            try:
                path_stem = '//*[@id="proxylisttable"]/tbody/tr['
                proxy_anonymity = driver.find_element_by_xpath(path_stem + str(i) + ']/td[5]').text
                if proxy_anonymity == 'elite proxy':
                    path_ip = path_stem + str(i) + ']/td[1]'
                    ip = driver.find_element_by_xpath(path_ip).text
                    path_port = path_stem + str(i) + ']/td[2]'
                    port = driver.find_element_by_xpath(path_port).text
                    lists.append([ip, port])
                i += 1
            except Exception as e:
                print("Ran into error", e)
                break
        for content in lists:
            ip_port = content[0] + ' ' + content[1] + '\n'
            with open('proxy_list.txt', 'w+') as file:
                    file.write(ip_port)
        driver.close()
