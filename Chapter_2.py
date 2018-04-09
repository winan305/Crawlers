from urllib.request import urlopen
# pip install beautifulsoup4
from bs4 import BeautifulSoup as bs

'''
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = bs(html, "html.parser")
# findAll(tagNaee, tagAtr)
nameList = bsObj.findAll("span", {"class":"green"})
for name in nameList :
    print(name.get_text())

nameList = bsObj.findAll(text="the prince")
print(len(nameList))
>>> 7
'''

'''
# find child
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = bs(html, "html.parser")

for child in bsObj.find("table", {"id":"giftList"}).children :
    print(child)
'''
'''
# find sibling
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = bs(html, "html.parser")

for sibling in bsObj.find("table", {"id":"giftList"}).tr.next_siblings :
    print(sibling)
'''

'''
# find parent
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = bs(html, "html.parser")
print(bsObj.find("img",{"src":"../img/gifts/img1.jpg"}).parent.previous_sibling.get_text())
# select img -> select parent tag(<td>) -> select previous_sibling -> select $15.00
'''

# regex example
import re
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = bs(html, "html.parser")
imgs = bsObj.findAll("img", {"src":re.compile("\.\.\/img\/gifts/img.*\.jpg")})
# ../img/gifts/img ~ .jpg
for img in imgs :
    print(img["src"])