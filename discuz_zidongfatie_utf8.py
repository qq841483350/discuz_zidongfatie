#coding:utf8
#discuz自动登陆并发帖   注意不要启用登陆验证码
import urllib2,urllib,cookielib,requests,re,time,xlrd,html2UBB,get_tags,random

def discuz(domain="网站域名注意前面 不带http:// 后面也不能事/",exclename='存放用户名密码的excel表格的名字如：username.xls',fid='栏目ID（栏目URL的forum-后面的第一个值）',subject='帖子标题',message='帖子内容',tags='帖子的关键词'):

    #---------------获取excle中提前准备好的用户名与密码---------------------
    data=xlrd.open_workbook(exclename)  #用xlrd打开excle表格,其中exclename为excle的文件名加后缀
    # table=data.sheets()[0]  #通过索引顺序获取
    table=data.sheet_by_index(0)  #通过索引顺序获取
    # table=data.sheet_by_name(u'Sheet1') #通过名称获取
    nrows=int(table.nrows)         #获取表格行数

    #----随机选择一个账号密码进行发布内容---
    list=[]
    for num in range(0,nrows):
        list.append(num)      #根据总共有多少个账号生成 一个列表
    x=random.sample(list,1)[0]    #生成一个随机数，那随即选取一个账号密码


    #---------------模拟头部信息------------------------
    headers={
        "Host":domain,      #网站域名 注意前面 不带http:// 后面也不能事/
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
    }


    #-----------保持账号密码登陆后的状态---------------------------
    cookieJar=cookielib.CookieJar()   # 初始化一个CookieJar来处理Cookie
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))    # 实例化一个全局opener
    urllib2.install_opener(opener)     #安装登陆信息到头部 使登陆后可以保持登陆状态

    username=table.cell(x,0).value.encode('utf8') #按座标（方块）获取数据 这里获取的是左边第x行第1列 用户名
    password=table.cell(x,1).value.encode('utf8') #按座标（方块）获取数据 这里获取的是左边第1行第2列的 密码

    #-------模拟登陆的数据-------
    login_data={
        "username":username,    #登陆用户名
        "password":password,  #登陆密码

    }
    #-----------模拟登陆数据结束-----------------

    login_data=urllib.urlencode(login_data)  #对登陆数据进行编码

    #-----登陆URL地址,可以通过抓包获得--------
    login_url="http://%s/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"%domain  #登陆地址url

    req=urllib2.Request(url=login_url,data=login_data,headers=headers) #获取cooie
    html=urllib2.urlopen(req).read() #带着cookie打开主页和下面的方法两种方式都可以
    #html=opener.open(req).read()  #带着cookie打开主页和上面的方法，两种方式都可以

    if """window.location.href""" in html:
        print '登陆成功,用户名是：'.decode('utf8'),username
        cookie=[]   #定义一个空列表
        for ck in cookieJar:     #cookie是一个对象，列表对象
            a=ck.name+'='+ck.value;   #把ck的列表的值与数字用
            cookie.append(a)        #添加到事先定义的列表里
        str=';'                      #定义一个字符串分号;
        cookie=str.join(cookie)      #把cookie列表里的每一个对像以 分号;分隔开来
        headers['Cookie']=cookie     #把登陆网站后获取到的cookie添加到头部header列表里，为了下面以登陆后的cookie来发表帖子

        #-----获取登陆安全验证formhash的值-------
        r=requests.get('http://%s'%domain,headers=headers)  #以登陆后的状态打开网站首页
        html=r.text   #网页源代码以text文本的形式打开
        formhash=re.findall('<input type="hidden" name="formhash" value="(.*?)" />',html)[0].encode('utf8')   #利用正则匹配到formhash的值
        #-----获取登陆安全验证formhash的值结束-------

        #---------开始获取关键词TAGS-----------
        tags=get_tags.get_tags(subject)
        message=html2UBB.Html2UBB(message)   #把获取到的帖子内容转换为discuz能够正常识别与显示的UBB代码
        post_data={
                "formhash":formhash,              #动态获取的formhash的值,
                "subject":subject,   #帖子标题
                "message":message,   #帖子内容
                "tags":tags,                    #关键词
                "topicsubmit":"发表帖子",      #表示发表帖子操作动作
                }

        #post_data=urllib.urlencode(post_data)  #对发表post数据进行编码

        #--发表帖子的URL-
        post_url="http://%s/forum.php?mod=post&action=newthread&fid=%s&extra="%(domain,fid)
        #fid就是栏目URL中forum-后面的数据或者字母（fid是变量默认是数字,有些在后台设置了别名也可以有是一个字符串）

        req=urllib2.Request(url=post_url,data=post_data,headers=headers)  #模拟一个发送帖子的cookie
        html=urllib2.urlopen(req).read()    #以模拟好的cookie发表帖子并返回发表帖子后的HTML
        if subject in html:
            print '发表成功标题是：'.decode('utf8'),subject
            #del headers['Cookie']
        elif subject not in html:
            print '发布失败,请检查您的用户名和密码是否正确:'.decode('utf8'),'用户名是：'.decode('utf8'),username
        else:
            pass
    elif '登录失败' in html:
        print '登陆失败,用户名是'.decode('utf8'),username,'直接跳过,继续执行'.decode('utf8')
    else:
        pass
if __name__=="__main__":
    domain="www.aixihuabbs.com"  #网站域名
    exclename='username.xls'
    fid="46"    #fid就是栏目URL中forum-后面的数据或者字母（fid是变量默认是数字,有些在后台设置了别名也可以有是一个字符串）
    subject="""seo搜索引擎优化是什么"""  #帖子标题
    message="""seo搜索引擎优化是什么""" #帖子内容

    discuz(domain,exclename,fid,subject,message)
