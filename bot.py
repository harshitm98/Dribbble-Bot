import requests
from lxml import html
import time
import random
import xlrd
import xlwt
from xlutils.copy import copy

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}




def login(username, password):
    #Todo: Implement proxy
    try:
        url = "https://www.dribbble.com/session/new"
        session = requests.Session()
        result = session.get(url)
        # Getting authenticity token
        tree = html.fromstring(result.text)
        token = str(tree.xpath('//input[@name="authenticity_token"]/@value'))
        token = token[2:-2]
        payload = {
            'login': username,
            'password': password,
            'authenticity_token': token,
            'utf-8': '✓'
        }
        post_url = "https://dribbble.com/session"
        req = session.post(post_url, data=payload, headers=headers)

        if int(req.status_code) == 200:
            print("Logged in...")
            listingOutPostsThatAreToBeLiked(username, token, session)
        else:
            print("Problem logging in...")
    except Exception as e:
        print("Error: ", e)


def writeToExcel(username, liked):
    try:
        book_original = xlrd.open_workbook('liked_post.xls')
        sheet_original = book_original.sheet_by_index(0)
        book = copy(book_original)
        sheet = book.get_sheet(0)
        rows = sheet_original.nrows
        for i in range(0, rows):
            if sheet_original.cell_value(i, 0) == username:
                sheet.write(i, 1, liked)
                return
        sheet.write(rows, 0, username)
        sheet.write(rows, 1, liked)
        book.save('liked_post.xls')
    except FileNotFoundError:
        wb = xlwt.Workbook()
        sheet = wb.add_sheet('Sheet One')
        sheet.write(0, 0, username)
        sheet.write(0, 1, liked)
        wb.save('liked_post.xls')


def listingOutPostsThatAreToBeLiked(username, token, session):
    handle_url = "https://dribbble.com/SumitH"
    result = session.get(handle_url)
    content = str(result.content)
    file = open("posts_liked", "a+")
    posts = []
    #Todo: Find a way to include posts that are behind loading more...
    while True:
        screenshot_start = content.find('id="screenshot-')
        screenshot_end = content.find('"', screenshot_start+len('id="screenshot-'))
        if screenshot_start != -1:
            posts.append(int(content[screenshot_start+len('id="screenshot-'):screenshot_end]))
            content = content[screenshot_end+1:]
        else:
            break
    request_url = "https://dribbble.com/harshitm98/likes/add"
    cookie = ""
    i = 0
    for key, value in requests.utils.dict_from_cookiejar(session.cookies).items():
        if i != 0:
            cookie = cookie + "; "
        cookie = cookie + key + "=" + value
        i += 1
    request_header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'cookie': cookie,
        'x-csrf-token': token
    }
    try:
        liked = []
        liked_posts = []
        try:
            wb = xlrd.open_workbook('liked_post.xls')
            sheet = wb.sheet_by_index(0)
            for i in range(0, sheet.nrows):
                if str(sheet.cell_value(i, 0)) == username:
                    liked_posts = str(sheet.cell_value(i, 1)).split(',')
        except Exception as e:
            print("File does not exists...", e)

        for post_id in posts:
            if str(post_id) in liked_posts:
                print("Already liked: ", post_id)
            else:
                payload = {
                    'screenshot_id': post_id
                }
                add = session.post(request_url, data=payload, headers=request_header)
                # time.sleep(random.choice[3,4,5,6,7,8,9])
                if add.status_code == 200:
                    print("Liked: ", post_id)
                    liked.append(post_id)
                else:
                    print("Encountered some error with: ", post_id)
            for i in liked:
                liked_posts.append(i)
            for i in range(0, len(liked_posts)):
                liked_posts[i] = str(liked_posts[i])
        writeToExcel(username, ','.join(liked_posts))
    except Exception as e:
        print("Error: ", e)
    file.close()


with open('credentials.txt') as file:
    credentials = file.read()
    credentials = credentials.split('\n')

with open('filled_up_dribbble.txt') as file:
    dribbble_accounts = file.read()
    dribbble_accounts = dribbble_accounts.split('\n')

# for credential in credentials:
#     credential = credential.split(' ')
#     while credential[2] in dribbble_accounts:
#         emailid = credential[2] + "@yandax.com"
#         password = credential[3]
#         login(emailid, password)
login('clarissabackman35338034@yandax.com', 'aJhzhrLVH3')
