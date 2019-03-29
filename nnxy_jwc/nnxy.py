from lxml import etree
import requests
from prettytable import PrettyTable
from bs4 import BeautifulSoup
import base64
from PIL import Image
import pytesseract
import re

print('南宁学院学生成绩查询工具')
url='http://jw.nnxy.cn/jsxsd'
C=requests.session()
r=C.get(url)
print(r.cookies.get_dict())

def getrandom():
    try:
        url='http://jw.nnxy.cn/jsxsd/verifycode.servlet'
        r=C.get(url)
        F=open('验证码.jpg','wb')
        F.write(r.content)
        F.close()
    except:
        print('未知错误')


def doLongin(encodeed):
    getrandom()
    img=Image.open('验证码.jpg')
    img.show()
	#验证码识别方法
    randomcode = pytesseract.image_to_string(img)
    print("ORC引擎识别验证码为：{}".format(randomcode))
    sub_str = re.sub("([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",randomcode)
    print("ORC引擎识别验证码为(过滤特殊字符)：{}".format(sub_str))
	#验证码识别模块
    random=input('请查看当前文件夹下的验证码图片手动输入验证码：')

    url='http://jw.nnxy.cn/jsxsd/xk/LoginToXk'

    Data={
            "encoded": encodeed,
            "RANDOMCODE": random
        }
    try:
        r=C.post(url,data=Data)
        r.raise_for_status()
        #print('登录成功！状态码为：',r.status_code)
    except:
        print('密码或验证码错误')
def decodeB64():
    count=input('学号:')
    passw=input('密码:')
    count=bytes.decode(base64.b64encode(str.encode(count)))
    passw=bytes.decode(base64.b64encode(str.encode(passw)))
    return '{}%%%{}'.format(count,passw)


def getGrade():
    encoded=decodeB64()
    doLongin(encoded)
    url='http://jw.nnxy.cn/jsxsd/kscj/cjcx_list'
    try:
        r=C.get(url)
        r=r.text
        req=BeautifulSoup(r,'lxml')
        all=req.find_all('div',class_='Nsb_pw')
        content=str(all[2])
        html=etree.HTML(content)


        print('平均绩点：',html.xpath('//span/text()')[0])
        table = PrettyTable(['序号','开课学期', '课程名称', '成绩', '学分', '绩点', '考核方式', '课程属性'])
        for item in html.xpath('//tr')[2:]:
            li=item.xpath('.//*/text()')
            table.add_row([li[0],li[1],li[3],li[4],li[5],li[7],li[8],li[-2]])
        print(table)
    except:
        print('密码或验证码错误/请按回车重新输入')
        input()


while True:
    getGrade()

