import requests
import os
from lxml import etree

head = {
    'Referer': 'https://e-hentai.org/?f_search=digatsukune&f_apply=Apply+Filter',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

def getList():

    url = 'https://e-hentai.org/?f_search=artist:kemono&f_apply=Apply+Filter'
    response = requests.get(url=url,headers = head)
    #print(response.text)
    html = etree.HTML(response.text)
    #comicList = html.xpath('/html/body/div[1]/div[2]/table[2]/tr')
    #当前页的所有漫画列表

    comicUrlList = html.xpath('/html/body/div[1]/div[2]/table[2]/tr/td[3]/div/div[3]/a/@href')
    comicNameList = html.xpath('/html/body/div[1]/div[2]/table[2]/tr/td[3]/div/div[3]/a/text()')


    for each in comicNameList:
        if not os.path.exists('./comic/'+each.replace('?','').replace('|','').replace('"','')):
           # dir = 'E:\PythonCode\e-hentai\comic\\'
            #print('不存在文件夹')
            print('创建文件夹：'+each)
            #dir = dir+each
            os.makedirs('./comic/'+each.replace('?','').replace('|','').replace('"',''))
        else:
            pass

    return comicUrlList,comicNameList

def getImageUrl(url):

    url_index = url+'?p=0'
    print(url_index)
    response = requests.get(url=url_index,headers=head)
    html = etree.HTML(response.text)
    #print(response.text)
    #当前页面的所有图片链接
    imageUrl=[]
    imageUrl = imageUrl + html.xpath('//*[@id="gdt"]/div/div/a/@href')
    page = html.xpath('/html/body/div[3]/table/tr/td')
    #print(imageUrl)
    print(len(page))
    if len(page) == '3':
        print('只有一页')

        #imageUrl =  html.xpath('//*[@id="gdt"]/div/div/a/@href')

        return imageUrl
    else:
        for i in range(len(page)-3):
            print('还有第二页:',i+1)
            url_index = url + '?p='+str(i+1)
            response = requests.get(url=url_index, headers=head)
            html = etree.HTML(response.text)
            #imageUrl = html.xpath('//*[@id="gdt"]/div/div/a/@href')
            imageUrl = imageUrl+html.xpath('//*[@id="gdt"]/div/div/a/@href')
        return imageUrl



def savaImage(imageContent,dir):
    try:
        F = open(dir,'wb')
        F.write(imageContent)
        F.close()
        print('保存到了:'+dir)
    except:
        print('保存失败.')

def getImage(imageUrl,dir):

    response = requests.get(url=imageUrl,headers=head)
    html = etree.HTML(response.text)
    imageContent = html.xpath('//*[@id="img"]/@src')
    #print(response.text)
    #print(imageContent)
    image = requests.get(url=imageContent[0],headers=head)
    savaImage(image.content,dir)
    #return image.content



#getList()
#getImageUrl('https://e-hentai.org/g/1291411/1ea0116dbc/')
#image=getImage('https://e-hentai.org/s/492feda435/1291411-1')
#savaImage(image)
if __name__ == "__main__":

    imageUrl = getImageUrl('https://e-hentai.org/g/1196656/554f09c0e2/')
    print(len(imageUrl))
    for e in range(len(imageUrl)):
        i_dir = './comic/'+'(Kansai! Kemoket 6) [Kaiten ParaDOGs (Diga Tsukune)] 1DK, Bokura to. | 恋人小公寓、与我俩。 [Chinese] [虾皮汉化组]'.replace('?','').replace('|','').replace('"','')+'/'+str(e+1)+'.jpg'
        getImage(imageUrl[e],i_dir)




