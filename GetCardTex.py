from bs4 import BeautifulSoup
from lxml import etree
import os
import requests
import urllib.request
import shutil 


url_base = "https://fategrandorder.fandom.com/"
url_servant_list= url_base + '/wiki/Servant_List_by_ID'

def DOM(url):
    req=requests.get(url)
    content=req.text
    soup=BeautifulSoup(content, "html.parser")
    return etree.HTML(str(soup))

start = len(os.listdir('./imgs'))
current = 0
first = True
for element in DOM(url_servant_list).xpath('//tbody/tr[td]'):
    current += 1
    if start - 1 >= current: continue
    
    id = element.xpath('td[4]')[0].text.strip()
    name = element.xpath('td[2]/a')[0].text.strip()

    if start != 0 and first: shutil.rmtree('./imgs/{}'.format(id))
    first = False
    if os.path.exists('./imgs/{}'.format(id)): shutil.rmtree('./imgs/{}'.format(id))
    os.mkdir('./imgs/{}'.format(id))
    tbody = DOM(url_base + element.xpath('td[2]/a')[0].attrib['href']).xpath("//div[contains(@class, 'wds-tab__content')][figure]")
    print('[{}] {}'.format(id, name))
    img_index = 1
    for e in tbody:
        if 'April Fool' not in e.xpath('figure/a')[0].attrib['title']:
            if '.webp' not in e.xpath('figure/a')[0].attrib['href'].lower(): continue
        print('\t- {} Image: {}'.format(img_index, e.xpath('figure/a')[0].attrib['title']))
        urllib.request.urlretrieve(e.xpath('figure/a')[0].attrib['href'], './imgs/{}/{}.png'.format(id, e.xpath('figure/a')[0].attrib['title'].replace('/', ' ')))
        img_index += 1
