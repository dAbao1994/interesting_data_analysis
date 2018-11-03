import urllib.request
import re
import urllib.error
import pymysql
import jieba.analyse

headers=('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0')
opener=urllib.request.build_opener()
opener.addheaders=[headers]
urllib.request.install_opener(opener)
for i in range(1,95):
    url="https://comment.mgtv.com/v4/comment/getCommentList?page="+str(i)+"&subjectType=hunantv2014&subjectId=4665374&callback=jQuery1820000054068137614993184_1541125725491&_support=10000000&_=1541126014617"
    conn = pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="mongotv")
    data = urllib.request.urlopen(url).read().decode()
    patnext='"nickName":"(.*?)",'
    name=re.compile(patnext).findall(data)
    patcom='"content":"(.*?)",'
    comment=re.compile(patcom).findall(data)
    for j in range(0,len(comment)):
        namedata=name[j]
        comdata=comment[j]
        tag = jieba.analyse.extract_tags(comdata, 3)
        print(namedata + "的评论:" + comdata)
        for k in range(0,len(tag)):
            tagdata=tag[k]
            print(tagdata)
            sql="insert into mongo(name,comment,tf)values('"+name[j]+"','"+comment[j]+"','"+tagdata+"')"
        conn.query(sql)
    conn.close()
    print("-----------------")
    print("第" + str(i) + "页爬取成功")


