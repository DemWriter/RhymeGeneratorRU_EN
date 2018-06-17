from bs4 import BeautifulSoup
from tabulate import tabulate
from google.cloud import translate
import requests

translate_client = translate.Client()

def translate(t,lan):
    return(translate_client.translate(t, target_language=lan)['translatedText'])

dic = {'ь':'', 'ъ':'', 'а':'a', 'б':'b','в':'v',
       'г':'g', 'д':'d', 'е':'e', 'ё':'yo','ж':'zh',
       'з':'z', 'и':'i', 'й':'y', 'к':'k', 'л':'l',
       'м':'m', 'н':'n', 'о':'o', 'п':'p', 'р':'r', 
       'с':'s', 'т':'t', 'у':'u', 'ф':'f', 'х':'h',
       'ц':'ts', 'ч':'ch', 'ш':'sh', 'щ':'sch', 'ы':'yi',
       'э':'e', 'ю':'yu', 'я':'ya'}

def get_rhymes_rus(w,u=None):
    url = 'https://rifme.net/r/'+w+'/'+str(u)
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
          }
    r = requests.get(url, headers = headers)

    soup = BeautifulSoup(r.text.encode('cp1251'), "lxml")

    rhymes = []

    try:
        for i in soup.find('ul', {'class': 'rifmypodryad'}):
            if(i==' '): continue
            i = [w for w in i]
            t = ''
            for j in i:
                try:
                    t+=j.text
                except:
                    t+=j
            if('https://rifme.net/'!=t):
                rhymes.append(t)
        return rhymes
    except:
        print('rhyme not found or need stress')
        return []
    
def get_rhymes_en(w):
    url = 'https://www.rappad.co/rhymes-with?utf8=%E2%9C%93&word='+w+'&commit=Find+Rhymes'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
          }
    r = requests.get(url, headers = headers)

    soup = BeautifulSoup(r.text, "lxml")

    rhymes = []

    try:
        for i in soup.find_all('div', {'class': 'columns large-4 small-6'}):
            if(i==' '): continue
            i = [w for w in i]
            t = ''
            for j in i:
                try:
                    t+=j.text.lower()
                except:
                    t+=j.lower()
            rhymes.append(t)
        return rhymes
    except:
        print('rhyme not found')
        return []

def sft(x,lan):
    c=0
    t,re=[],[]
    for j in x:
        t.append([j,translate(j,lan)])
        if(c>3):
            c=0
            re.append(t)
            t=[]
        c+=1
    return re

def tr(x):
    t = ''
    for i in x:
        t+=dic.get(i.lower(), i.lower()).upper() if i.isupper() else dic.get(i, i)
    return t

while(1):
    i = input('<< ')
    print('English rhymes: ')
    print(tabulate(sft(get_rhymes_en(tr(i)),'ru')))
    print('\n\n')

    print('Russian rhymes: ')
    print(tabulate(sft(get_rhymes_rus(i),'en')))
    print('\n\n')

