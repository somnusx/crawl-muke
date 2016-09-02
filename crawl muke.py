import re
import os
import thre
import requests
from pyquery import PyQuery as q


def fit3_1(url):
    s = q(url, headers=headers)
    r = s('div').filter('.moco-course-wrap')
    for i in r:
        link = re.findall(r'learn/\d{1,6}(?=")', str(q(i)))
        if link:
            ur = 'http://www.imooc.com/' + link[-1]
            print(ur)
            fit2(ur)

def fit4(url):
    s = q(url, headers=headers)
    r = s('div').filter('.item')
    link = re.findall(r'c=.+?(?=")', str(r))
    for li in link:
        url = 'http://www.imooc.com/course/list?' + li
        print(url)
        fit3(url)


def fit3(url):
    s = q(url, headers=headers)
    r = s('div').filter('.page')
    if r:
        pages = re.findall(r'\d', str(r.text()))
        for page in pages:
            urls = url + '&page=' + page
            fit3_1(urls)
    else:
        fit3_1(url)



def fit2(url):
    s = q(url, headers=headers)
    r = s('div').filter('.chapter ')
    name1 = s('h2').text()
    for i in r:
        a = q(i)
        name2 = re.findall(r'第\d.+?(?=&)',str(a))
        link = a('a').filter('.J-media-item')
        for i in link:
            link = re.findall(r'(?<=video/).+?(?=")', str(q(i)))
            b = q(i).text()
            name3 = re.findall(r'\d-\d.+(?=\r)', str(b))
            if link:
                url = 'http://www.imooc.com/course/ajaxmediainfo/?mid=' + link[-1] + '&mode=flash'
                r = requests.get(url)
                r = r.json()
                r = r['data']['result']['mpath']
                H = r[-1]#BD
                M = r[-2]#HD
                L = r[-3]#SD
                mkdr = '.\\' + name1 + '\\' + name2[-1]
                if os.path.exists(mkdr)==False:            
                    os.makedirs(mkdr)
                name = name1 + '\\' + name2[-1] + '\\' + name3[-1] + '.mp4'
                thre.download( H, name, blocks=3, proxies={} )
             

def fit1(url):
    link = url.split('/', -1)[-1]
    ul = 'http://www.imooc.com/course/ajaxmediainfo/?mid=' + link + '&mode=flash'
    s = q(url, headers=headers)
    r = s('em').text()
    video = re.findall(r'\d-.+?(?=\d)', r)
    name = video[-1] + '.mp4'
    r = requests.get(ul)
    r = r.json()
    r = r['data']['result']['mpath']
    H = r[-1]#BD
    M = r[-2]#HD
    L = r[-3]#SD
    thre.download( H, name, blocks=4, proxies={} )


def ur(url):
    if url =='http://www.imooc.com/':
        print('fit4')
        fit4(url)
    elif url.split('/',-1)[-2] == 'video':
        print('fit1')
        fit1(url)
    elif url.split('/',-1)[-2] == 'learn':
        print('fit2')
        fit2(url)
    else:
        print('fit3')
        fit3(url)

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
print('请输入链接地址：',end="")
url = input()
ur(url)

