import requests
import bs4
import os
from PIL import Image

#使用图片库PTL
#构造登录需要提交的内容
#设置登录请求头并建立一个session

loginUrl = 'http://elite.nju.edu.cn/jiaowu/'
loginDoUrl = "http://elite.nju.edu.cn/jiaowu/login.do"
loginHostUrl = 'elite.nju.edu.cn'
loginReferer = "http://elite.nju.edu.cn/jiaowu/exit.do"
indexUrl = 'http://elite.nju.edu.cn/jiaowu/student/studentinfo/index.do'

head = {
        'Upgrade-Insesure-Requests': '1',
        'Connection': 'keep-alive',
        'Host': loginHostUrl,
        'Referer': loginReferer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
        }

loginSession = requests.Session()
loginHtml = loginSession.get(loginUrl, headers=head, allow_redirects = False)

def createPostContent(Url):
    #创建需要post的data
    #使用lxml的html解析器
    startSoup = bs4.BeautifulSoup(loginHtml.text, 'lxml')
    # 找到验证码图片地址
    Source = startSoup.find('img', attrs={'id': 'ValidateImg'})['src']
    # 下载验证码图片
    pic = loginSession.get(
        Url + Source).content
    with open('validateImg.png', 'wb') as f:
        f.write(pic)
    # 打开验证码图片
    image = Image.open('{}/ValidateImg.png'.format(os.getcwd()))
    image.show()
    # 构造需要提交的参数列表
    Data = {'userName': '', 'password': '',
            'ValidateCode': input('请输入图片中的验证码：')
            }
    return Data

#获取登录数据
data = createPostContent(loginUrl)

# 模拟登录教务系统
loginSession.post(loginDoUrl, data = data, headers = head)
print(loginSession.cookies)
test = loginSession.get(indexUrl)

#获取登录后页面信息
print(loginSession.cookies)
soup = bs4.BeautifulSoup(test.text, 'lxml')
print(soup.text)

#获取学生姓名，验证登录成功与否
try:
    name = soup.find('div', attrs={'id': 'UserInfo'}).text
except:
    name = '登录失败'
print(name)
