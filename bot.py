import requests
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0'
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
            listingOutPostsThatAreToBeLiked(token, session)
        else:
            print("Problem logging in...")
    except Exception as e:
        print("Error: ", e)


def listingOutPostsThatAreToBeLiked(token, session):
    handle_url = "https://dribbble.com/SumitH"
    result = session.get(handle_url)
    content = str(result.content)
    file = open("posts_liked", "a+")
    posts = []
    liked = []
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
        'User-Agent': 'Mozilla/5.0',
        'cookie': cookie,
        'x-csrf-token': token
    }
    try:
        f = open('posts_liked', 'r')
        liked_posts = f.read().split('\n')
        for post_id in posts:
            if str(post_id) in liked_posts:
                print("Aleardy liked: ", post_id)
            else:
                payload = {
                    'screenshot_id': post_id
                }
                add = session.post(request_url, data=payload, headers=request_header)
                if add.status_code == 200:
                    file.write(str(post_id))
                    file.write("\n")
                    print("Liked: ", post_id)
                else:
                    print("Encountered some error with: ", post_id)
    except Exception as e:
        print("Error: ", e)

    file.close()



login('maheshwari.hsushil2016@vitstudent.ac.in', 'harshit123')

