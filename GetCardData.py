from dataclasses import replace
from email.encoders import encode_noop
from time import thread_time
from bs4 import BeautifulSoup
from lxml import etree
import os
import requests
import json

def ReturnStringATKHPFormatted(s):
    arr = []
    b = 1
    def IndexOfN(string, sub, n):
        start = string.find(sub)
        while start >= 0 and n > 1:
            start = string.find(sub, start+len(sub))
            n -= 1
        return start
    if '★' in s:
        arr.append(s[0:s.index('★')-1])
        for i in range(s.count('★')):
            arr.append(s[IndexOfN(s, '★', b)-1:IndexOfN(s, '★', b+1) if IndexOfN(s, '★', b+1) != -1 else len(s)])
            b += 1
    else: arr.append(s[0:len(s)])
    result = ''
    for a in arr: result += a + ' | '
    return result[:-3]

class CardData: 
    def __init__(self):
        self.Id = 0
        self.Name = ''
        self.Japanese = ''
        self.Class = ''
        self.Servant = 0
        self.Stars = 0
        self.Gold = False
        self.Cost = 0
        self.Attribute = 0
        self.Gender = ''
        self.Alignments = ''

url_base = "https://fategrandorder.fandom.com/"
url_servant_list= url_base + '/wiki/Servant_List_by_ID'

def DOM(url):
    req=requests.get(url)
    content=req.text
    soup=BeautifulSoup(content, "html.parser")
    return etree.HTML(str(soup))

start = len(os.listdir('./datas'))
current = 0
for element in DOM(url_servant_list).xpath('//tbody/tr[td]'):
    current += 1
    if start >= current: continue
    card = {}
    try:
        tbody = DOM(url_base + element.xpath('td[2]/a')[0].attrib['href']).xpath('//tbody')[1]
        card = { 'Id' : 0, 'Name' : '', 'Japanese' : '', 'Star' : 0, 'Cost' : 0, 'Class' : '', 'Type' : 0, 
            'ATK' : '', 'HP' : '', 'GrailATKLV100' : '', 'GrailATKLV120' : '',
            'GrailHPLV100' : '', 'GrailHPLV120' : '', 'AKA' : '', 'Alignments' : '', 'Growth' : '', 'Attribute' : '', 'Gender':'', 'Traits': ''}
        card["Id"] = element.xpath('td[4]')[0].text.strip()
        card["Name"] = element.xpath('td[2]/a')[0].text.strip()
        card["Star"] = element.xpath('td[3]')[0].text.count('★')
        
        card["Class"] = tbody.xpath("//*[@class='ServantInfoClass']/a")[0].attrib['title']
        card["Type"] = 0
        
        #card["Japanese"] = tbody.xpath('tr[1]/td/span')[0].text
        #card["Alignments"] = ''.join(tbody.xpath("tr[11]/td[2]")[0].itertext()).replace('Alignments:', '').strip()
        #card["Gender"] = ''.join(tbody.xpath("tr[12]/td[1]")[0].itertext()).replace('Gender:', '').strip()
        #card["Cost"] = ''.join(tbody.xpath("tr[3]/td[2]")[0].itertext()).replace('Cost:', '').strip()
        #card["Attribute"] = ''.join(tbody.xpath("tr[8]/td[1]")[0].itertext()).replace('Attribute:', '').strip()
        b = False
        for tr in tbody.xpath('tr'):
            for td in tr.xpath('td'):
                if b: break
                td_txt = ''.join(td.itertext()).replace(u'\xa0', u' ')
                if 'Japanese Name:' in td_txt: card["Japanese"] = td_txt.replace('Japanese Name:', '').strip()
                elif 'ATK:' in td_txt and '/' in td_txt and not 'Grail' in td_txt and not 'NP' in td_txt: card["ATK"] = ReturnStringATKHPFormatted(td_txt).replace('ATK:', '').replace('  ', ' ').strip()
                elif 'HP:' in td_txt and '/' in td_txt and not 'Grail' in td_txt: card["HP"] = ReturnStringATKHPFormatted(td_txt).replace('HP:', '').replace('  ', ' ').strip()
                elif 'Lv.100 Grail ATK:' in td_txt: card["GrailATKLV100"] = td_txt.replace('Lv.100 Grail ATK:', '').strip()
                elif 'Lv.120 Grail ATK:' in td_txt: card["GrailATKLV120"] = td_txt.replace('Lv.120 Grail ATK:', '').strip()
                elif 'Lv.100 Grail HP:' in td_txt: card["GrailHPLV100"] = td_txt.replace('Lv.100 Grail HP:', '').strip()
                elif 'Lv.120 Grail HP:' in td_txt: card["GrailHPLV120"] = td_txt.replace('Lv.120 Grail HP:', '').strip()
                elif 'AKA:' in td_txt: card["AKA"] = td_txt.replace('?', '').replace('AKA:', '').strip()
                elif 'Alignments:' in td_txt: card["Alignments"] = td_txt.replace('Alignments:', '').strip()
                elif 'Cost:' in td_txt: card["Cost"] = td_txt.replace('Cost:', '').strip()
                elif 'Growth Curve:' in td_txt: card["Growth"] = td_txt.replace('Growth Curve:', '').strip()
                elif 'Attribute:' in td_txt: card["Attribute"] = td_txt.replace('Attribute:', '').strip()
                elif 'Gender:' in td_txt: card["Gender"] = td_txt.replace('Gender:', '').strip()
                elif 'Traits:' in td_txt: 
                    card["Traits"] = td_txt.replace('Traits:', '').strip()
                    b = True
            if b: break
    except Exception as e: 
        raise e
    print('[{}] {}★ {}\t - {} - ATK: {}'.format(card['Id'], card['Star'], card['Class'], card["Name"], card['ATK']))
    with open("./datas/{}.json".format(card['Id']) , "w", encoding='utf-8') as write:
        json.dump( card , write, ensure_ascii=False )