from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import re
import string


def cleanInput(input) :
    input = re.sub('\n+', " ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split()
    for item in input :
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i') :
            cleanInput.append(item)
    return cleanInput

# p.144~145 함수 교체해야함. 챕터8에 있는 ngrams 함수로.
def ngrams(input, n) :
    input = cleanInput(input)
    output = {}
    for i in range(len(input)-n+1) :
        ngramTemp = " ".join(input[i:i+n])
        if ngramTemp not in output :
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = bs(html, "html.parser")
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()
ngrams = ngrams(content,2)
ngrams = OrderedDict(sorted(ngrams.items(), key = lambda t:t[1], reverse=True))
print(ngrams)