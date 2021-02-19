# -*- coding: utf-8 -*-

from requests import Session
from bs4 import BeautifulSoup
from urllib3 import encode_multipart_formdata
from datetime import datetime,timedelta
from re import findall
from _thread import start_new_thread 
from time import time,localtime,strftime
import os
parm = eval(os.environ['PARM'])
tmp = datetime.today()+timedelta(hours=8)
today = tmp.strftime("%Y-%m-%d")
log = []


def sentMsg(msg, key):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = "https://sc.ftqq.com/key.send?text='.urlencode('msg')"
    return requests.post(api_url, headers=headers, timeout=None).content

def report(usr,pas,key,proxy):
    sess = Session()
    sess.headers['Content-Type'] = 'multipart/form-data; boundary=\
        ----WebKitFormBoundary5lPtCfVeRqiu7n6h'
    sess.headers['Host'] = 'yiqing.ctgu.edu.cn'
    sess.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    sess.headers['Connection'] =  'keep-alive'
    sess.headers['X-Requested-With'] = 'XMLHttpRequest'
    sess.headers['Upgrade-Insecure-Requests'] = '1'
    sess.headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6'
    sess.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;\
        q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    r=sess.get('http://yiqing.ctgu.edu.cn/wx/index/login.do?currSchool=ctgu&CURRENT_YEAR=2019&showWjdc=false&studentShowWjdc=false')
    
    proxies = {
    'http': proxy,
    'https': proxy
    }
     yiqingSession = requests.session()
    
    data=encode_multipart_formdata({'username':usr,'password':pas},
                                   '----WebKitFormBoundary5lPtCfVeRqiu7n6h')
    login=sess.post('yiqing.ctgu.edu.cn/wx/health/main.do',data=data[0])
    
    if(login.text!='success'):
        log.append([[usr,pas],usr])
        #return 0

    try:
        responseRes = yiqingSession.post(
            logUrl, data=postData,headers =header,timeout=None, proxies=proxies)
    except:
        sentMsg('网页无响应/请更换代理', key)
        
    r=sess.post('http://yiqing.ctgu.edu.cn/wx/health/studentHis.do')
    his=eval(r.text.replace('null','None'))
    r=sess.get('http://yiqing.ctgu.edu.cn/wx/health/toApply.do')
    apply={
        'province':'',
        'city':'',
        'district':'',
        'adcode':'',
        'longitude':'',
        'latitude':'',
        'sfqz':'',
        'sfys':'',
        'sfzy':'',
        'sfgl':'',
        'status':'',
        'sfgr':'',
        'szdz':'',
        'sjh':'',
        'lxrxm':'',
        'lxrsjh':'',
        'sffr':'',
        'sffy':'',
        'sfgr':'',
        'qzglsj':'',
        'qzgldd':'',
        'glyy':'',
        'mqzz':'',
        'sffx':'',
        'qt':'',
    }
    
     # 获取必要信息填入表单
    soup = BeautifulSoup(responseRes.text, "html.parser")
    getFormlist = soup.find_all('input')[0:15]
    
    if his[0]['sbrq']!=today:
        for key in apply:
            apply[key] = his[0][key] if his[0][key]!=None else ''
        apply['ttoken']=findall('ttoken" value="(.*?)"',r.text) or findall('stoken=(.*?)&',r.url)[0]
        del sess.headers['Content-Type']
        r=sess.post('http://yiqing.ctgu.edu.cn/wx/health/saveApply.do',data=apply)
        log.append([[usr,pas],strftime("%Y-%m-%d %H:%M:%S",localtime(his[0]['scrq']/1000))+' '+eval(r.text)["msgText"]+' '+his[0]['xm']])
    else:
        log.append([[usr,pas],strftime("%Y-%m-%d %H:%M:%S",localtime(his[0]['scrq']/1000))+' 已上报  '+his[0]['xm']])
    sess.close()
     responseRes = yiqingSession.post(
         postFormurl, data=postData,headers =header, verify=False, timeout=None, proxies=proxies)
     print(responseRes.text)
     sentMsg(username + ':'+ responseRes.text, key)
stime = time()

for usr,pas,key,proxy in parm:
    sentOne(username, password, key,proxy)
    #start_new_thread(report,(usr,pas,))
    report(usr,pas)
    #print(log[-1][-1])
while True:
    if len(log)==len(parm):
        for i in sorted(log,key=lambda x:parm.index(x[0])):
            print(i[0][0],i[1])
        break
    elif time()-stime>20:
        for i in sorted(log,key=lambda x:parm.index(x[0])):
            print(log[1])
        print('time')
        break
