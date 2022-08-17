from bs4 import BeautifulSoup, Comment
import requests
import re
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import os
import time
class Item:

    def __init__(self, title, url, thumbnail=None, contentTitle=None, infoLabels = None, server=None, v_id = None):
        self.title=title 
        self.url=url
        self.thumbnail=thumbnail 
        self.contentTitle=contentTitle
        self.infoLabels = infoLabels
        self.server = server
        self.v_id = v_id


def get_moovie_list():

    itemlist = []

    page = requests.get("https://ww1.cuevana3.me/?s=breaking")
    soup = BeautifulSoup(page.content, 'html.parser')

    matches = soup.find("ul", class_="MovieList").find_all("li", class_="xxx")

    for elem in matches:
        #thumb = elem.find("img").img["src"] 
        thumb = elem.find("img", class_="lazy attachment-thumbnail size-thumbnail wp-post-image")["data-src"]
        
        title = elem.find("h2", class_="Title").text
        url = elem.a["href"]
        year = elem.find("span", class_="Year").text
        print(thumb, title, url, year)
        itemlist.append(Item(title=title, url=url,thumbnail=thumb, contentTitle=title, infoLabels={'year': year}))


    print(itemlist)

def find_single_match(data, pattern, index=0):
    try:
        matches = re.findall(pattern, data, flags=re.DOTALL)
        return matches[index]
    except Exception:
        return ""


def findvideos():
    itemlist = []
    servers_list = {"1": "directo", "2": "streamtape", "3": "fembed", "4": "netu"}
    page = requests.get("https://ww1.cuevana3.me/21711/joker")
    soupx = BeautifulSoup(page.content, 'html.parser')
    
    
    soup = soupx.find("div", class_="TPlayer embed_div")

    matches = soup.find_all("div", class_="TPlayerTb")
    for elem in matches[:-1]:
        srv = servers_list.get(elem["id"][-1], "directo")
        elem = elem.find("iframe")
        url = "https:"+elem["data-src"]
        v_id = find_single_match(url, '\?h=(.*)') 

        if url:
            print("\n",url)
            itemlist.append(Item(title="%s", url=url,  server=srv.capitalize(), infoLabels="", v_id = v_id))
            #play(itemlist[0])
            #break
    #print(itemlist)

domain = "cuevana3.me"
domain_fix = "cuevana3.me"

headers = {"Content-Type": "Content-Type: application/x-www-form-urlencoded",
"Host": "api.cuevana3.me",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
"Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
"Accept-Encoding": "gzip, deflate, br",
"Origin": "null",
"DNT": "1",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "cross-site",
"TE": "trailers",
"Pragma": "no-cache",
"Cache-Control": "no-cache"
}
def play(item):
    item.server = ""

    if domain_fix in item.url or "tomatomatel" in item.url:
        page = requests.get(item.url)
        soupx = BeautifulSoup(page.content, 'html.parser')
        fix_url = soupx.find("a", class_="link")["href"]
        fix_url = get_urls(fix_url, item.v_id)
        responses = requests.get(fix_url)

        fix_url = get_urls(fix_url, item.v_id)
        fix_url = get_urls(fix_url, item.v_id)
        urlx = "https://api.%s/ir/redirect_ddh.php" % domain 
        myobj = {'url': item.v_id}
        myobjx = "url="+item.v_id
        x = requests.post(urlx, headers=headers, data=myobj)
        print("JSON Response ", x.status_code)
        opts = Options()
        opts.headless = False
        diract = os.path.dirname(os.path.abspath(__file__)) #Directorio donde se encuentra el script
        browser = Firefox(executable_path=diract+"/assets/geckodriver.exe", options=opts)
        urlgetx = fix_url
        browser.get(urlgetx)
        time.sleep(8)
        xlement = browser.execute_script("""
        var e = document.querySelector("img").click();
        """)
        time.sleep(0.5)        
        wx = browser.window_handles[1]
        browser.switch_to.window(window_name=wx)
        browser.close()
        browser.switch_to.window(browser.window_handles[0] )

        time.sleep(1.5)        
        element = browser.find_element_by_class_name('jw-video').get_attribute("src")
        print("aa",element)
        browser.close()
    return print("aa",element)


def get_urls(url, v_id):

    base_url = "https://api.%s/ir/rd.php" % domain
    param = 'url'

    if '/sc/' in url:
        base_url = "https://api.%s/sc/r.php" % domain
        param = 'h'

    if 'goto_ddh.php' in url:
        base_url = "https://api.%s/ir/redirect_ddh.php" % domain

    if 'goto.php' in url:
        base_url = "https://api.%s/ir/goto.php" % domain

    url = base_url + "?h=" + v_id

    return url


findvideos()
