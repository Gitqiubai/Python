import requests
from lxml import etree
import os
import time
import sqlite3
from multiprocessing import Pool,Process

head = {
    'Referer': 'https://e-hentai.org/?f_search=digatsukune&f_apply=Apply+Filter',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

def sqlDB():
    con = sqlite3.connect('comic.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists ComicName(id integer not null primary key autoincrement ,name char(255) not null )')
    cursor.execute('create table if not exists ImageName(id integer not null primary key autoincrement ,name char(255) not null )')
    con.commit()
    con.close()


def getList(word):

    #url = 'https://e-hentai.org/?f_search=digatsukune&f_apply=Apply+Filter'
    url = 'https://e-hentai.org/?page=0&f_search={}&f_apply=Apply+Filter'.format(word)
    response = requests.get(url=url,headers = head)
    #print(response.text)
    html = etree.HTML(response.text)
    #comicList = html.xpath('/html/body/div[1]/div[2]/table[2]/tr')
    #当前页的所有漫画列表

    comicUrlList = html.xpath('/html/body/div[1]/div[2]/table[2]/tr/td[3]/div/div[3]/a/@href')
    comicNameList = html.xpath('/html/body/div[1]/div[2]/table[2]/tr/td[3]/div/div[3]/a/text()')


    for each in comicNameList:
        #print(each)
        dir_name = each.replace('?','').replace('|','').replace('"','').replace('*','').replace('<','').replace('>','').replace(':','')
        if not os.path.exists('./comic/'+dir_name):
           # dir = 'E:\PythonCode\e-hentai\comic\\'
            #print('不存在文件夹')
            print('创建文件夹：'+dir_name)
            #dir = dir+each
            os.makedirs('./comic/'+dir_name)
        else:
            pass

    return comicUrlList,comicNameList


def getImageUrl(url):

    url_index = url+'?p=0'
    #print(url_index)
    response = requests.get(url=url_index,headers=head)
    html = etree.HTML(response.text)
    #print(response.text)
    #当前页面的所有图片链接
    imageUrl=[]
    imageUrl = imageUrl + html.xpath('//*[@id="gdt"]/div/div/a/@href')
    page = html.xpath('/html/body/div[3]/table/tr/td')
    #print(imageUrl)
    #print(len(page))
    if len(page) == '3':
        print('----只有一页')

        #imageUrl =  html.xpath('//*[@id="gdt"]/div/div/a/@href')

        return imageUrl
    else:
        for i in range(len(page)-3):
            print('----正在获取第[{}]页数据'.format(i+1))
            url_index = url + '?p='+str(i+1)
            response = requests.get(url=url_index, headers=head)
            html = etree.HTML(response.text)
            #imageUrl = html.xpath('//*[@id="gdt"]/div/div/a/@href')
            imageUrl = imageUrl+html.xpath('//*[@id="gdt"]/div/div/a/@href')
        return imageUrl


def savaImage(imageContent,dir):

    F = open(dir,'wb')
    F.write(imageContent)
    F.close()
    print('----保存到了:'+dir)
    con = sqlite3.connect('comic.db')
    cursor = con.cursor()
    cursor.execute('insert into ImageName (name) values ("{}")'.format(dir))
    con.commit()
    con.close()


def getImage(imageUrl,dir):

    try:
        response = requests.get(url=imageUrl,headers=head)
        html = etree.HTML(response.text)
        imageContent = html.xpath('//*[@id="img"]/@src')
        #print(response.text)
        #print(imageContent)
        image = requests.get(url=imageContent[0],headers=head)
        savaImage(image.content,dir)
        #设置休息时间
        time.sleep(0)
        #return image.content
    except:
        print('这里被Bang了')



#getList()
#getImageUrl('https://e-hentai.org/g/1291411/1ea0116dbc/')
#image=getImage('https://e-hentai.org/s/492feda435/1291411-1')
#savaImage(image)

if __name__ == "__main__":
    sqlDB()
    #设置搜索的关键词
    word = 'artist:kemono'
    comicUrlList,comicNameList = getList(word)
    print(comicUrlList,comicNameList)
    for i  in range(len(comicUrlList)):
        con = sqlite3.connect('comic.db')
        cursor1 = con.cursor()
        dir_name = comicNameList[i].replace('?', '').replace('|', '').replace('"', '').replace('*', '').replace('<','').replace('>', '').replace(':', '')
        print("开始爬取【{}】".format(dir_name))
        N=cursor1.execute('select name from ComicName where name = "{}"'.format(dir_name)).fetchall()
        if N:
            print('----数据已经存在了')
            con.close()
            continue
        imageUrl = getImageUrl(comicUrlList[i])
        #print(imageUrl)
        p = Pool(4)
        for e in range(len(imageUrl)):
            con = sqlite3.connect('comic.db')
            cursor2 = con.cursor()
            i_dir = './comic/'+dir_name+'/'+str(e+1)+'.jpg'
            im = cursor2.execute('select name from ImageName where name="{}" '.format(i_dir)).fetchall()
            if im:
                continue
            else:
                getImage(imageUrl[e],i_dir)

        print('\n当前漫画 保存完成')
        con = sqlite3.connect('comic.db')
        cursor = con.cursor()
        cursor.execute('insert into ComicName (name) values ("{}")'.format(dir_name))
        con.commit()
        con.close()



