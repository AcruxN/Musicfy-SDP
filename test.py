from http import cookies
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pprint

session = HTMLSession()
url = 'https://media1.vocaroo.com/mp3/1eHQ3wTJKFZ8'
# url = 'https://vocaroo.com/upload'
# url = 'https://google.com/'
session_cookies = session.cookies
my_cookie_jar = {'Name' : '__gads', 'Value':'ID=391a4c9322af58be-221ea5a8c1d0005c:T=1646015597:RT=1646015597:S=ALNI_MZ0qBQVteKoAm-yCs3s1zyc8gTYNA', 'Domain':'.vocaroo.com', 'Path': '/'}
res = session.get(url)

def get_download_link(url):
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url, cookies=my_cookie_jar)
    # for javascript driven website
    
    res.html.render()
    soup = BeautifulSoup(res.html.html, "html.parser")
    b = soup.find("a", class_="Button__button")
    return b.get('href')

def get_download_page(url):
    # GET request
    res = session.get(url)
    # for javascript driven website
    res.html.render(cookies=my_cookie_jar)
    # soup = BeautifulSoup(res.html.html, "html.parser")
    session.get_redirect_target(res)

def download_song(url):
    download = session.get(url, cookies=my_cookie_jar)
    open('test.mp3','wb').write(download.content)

# print(get_download_link(url))
# download = get_download_link(url)
download_song(url)