import re
import urllib.request
import sys
from bs4 import BeautifulSoup
# find all urls belongs to a teacher
page = urllib.request.urlopen('https://ese.nju.edu.cn/30444/list.htm')
htmlContent = page.read().decode('utf-8')
matchUrl = "http:\/\/ese.nju.edu.cn\/[a-z]+[_][0-9]+\/list.htm"
teacherUrl = re.findall(matchUrl, htmlContent)

# find teachers contains keywords
# keywords = ['微电子', '电路设计', '器件', '工艺技术', '材料制备','自动测试', '封装']
keywords = ['微电子']
for key in keywords:
    print(key)

electroTeachers = set()

for url in teacherUrl:
    teacherPage = urllib.request.urlopen(url)
    # extract class="text" of content, containing teachers' CV
    parsed_html = BeautifulSoup(teacherPage.read().decode('utf-8'), "html.parser")
    cvSet = parsed_html.body.find_all('div', attrs={'class':'text'})
    content = ""
    # convert bs4 object into str
    for text in cvSet:
        content += str(text)
    # judge whether keyword in text
    for key in keywords:
        if key in content:
            electroTeachers.add(url)

print("\n".join(electroTeachers))
print("Total: " + str(len(electroTeachers)))