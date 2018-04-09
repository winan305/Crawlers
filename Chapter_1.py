from urllib.request import urlopen
# pip install beautifulsoup4
from bs4 import BeautifulSoup as bs
# 404, 500 Error Handling
from urllib.request import HTTPError

def getTitle(url) :
    try :
        html = urlopen(url)
    except HTTPError as e :
        return None

    try :
        bsObj = bs(html.read(), "html.parser")
        title = bsObj.body.h1
    except AttributeError as e :
        return None
    return title

title = getTitle("http://pythonscraping.com/pages/page1.html")
if title == None : print("Title could not be found")
else : print(title)