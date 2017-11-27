#
#       爬行 民非网
#       target:http://www.synpo.gov.cn/cms/primitSearch.jspx?currentPage=1，http://www.synpo.gov.cn/cms/yearcheckSearch.jspx?currentPage=1
#

import requests
from bs4 import BeautifulSoup
import re
import xlsxwriter
import time
import random
import db_kit
import logging

domain = 'http://www.synpo.gov.cn'
targets = ['http://www.synpo.gov.cn/cms/primitSearch.jspx',"http://www.synpo.gov.cn/cms/yearcheckSearch.jspx"]
headers = [{"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"},
           {
               "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
           {
               "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
           {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"},
           {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"},
           {
               "User-Agent": "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}]

def getMainHTML(target,mf_tpe):
    # session=requests.session()
    params={"currentPage":1,"type":"2"}

    res = requests.get(target, params=params, headers=random.sample(headers, 1)[0]);
    # cookie=res.cookies;
    soup = BeautifulSoup(res.content, 'lxml')
    trs = None
    page=soup.find('div',class_='paging').find_all('span')
    recordCount=re.sub('\D',"",page[1].get_text())
    recordCount=recordCount[1:recordCount.__len__()]
    for i in range(108,int(recordCount)+1):
        print("爬取第 %d 页的数据"%(i) )
        params={"currentPage":i,"type":"2"}
        res = requests.get(target, params=params, headers=random.sample(headers, 1)[0]);
        if(res.status_code==200 and res.text.find("400 Bad Request")==-1):
            soup = BeautifulSoup(res.content, 'lxml')
            trs = soup.find('table').find_all('tr')
        else:
            logging.error("爬行目标  %s 出现解析错误"%(target))
            continue
        ret =None
        info=[]
        mf=None
        if(trs):
            for index,tr in enumerate(trs):
                if index==0:
                    continue
                else:
                    a=tr.find("a")
                    url=a["href"]
                    txt=a.get_text()
                    ret=db_kit.findMFOnByUrl(url,mf_tpe);
                    if ret is None :
                        info=getDetailHtml(url)
                        mf=db_kit.Mf()
                        mf.type=mf_tpe
                        mf.catalog=str(info[0]).replace("\r\n","").replace("\t","").strip()
                        mf.reg_time=info[1]
                        mf.reg_org=info[2]
                        mf.reg_num=info[3]
                        mf.legal=info[4]
                        mf.mng_unit=str(info[5]).replace("\r\n","").replace("\t","").strip()
                        mf.expiry_date=str(info[6]).replace("\r\n","").replace("\t","").strip()
                        mf.scope=info[7]
                        mf.ads=info[8]
                        mf.zip_code=info[9]
                        mf.tel=info[10]
                        mf.phone=info[11]
                        mf.url=url
                        mf.reg_name=txt
                        db_kit.insert(mf)
                        time.sleep(0.5)
                    elif ret and not ret.reg_name:
                        print("执行了更新操作")
                        ret.reg_name = txt
                        db_kit.update(ret)
                    else:
                        print("数据已经存在， %s "%(ret.reg_name))




def getDetailHtml(url):
    # proxy = requests.get('http://localhost:5010/get').text
    # proxies = {"http": proxy}
    bl = True
    res = None;
    while (bl):
        print('爬行的URL>>' + domain + url)
        # print('使用的代理为>>' + str(proxies))
        try:
            res = requests.get(domain + url, params=None, headers=random.sample(headers, 1)[0],
                               # proxies=proxies,
                               timeout=6)
            if res.status_code==200 and res.text != '' and res.text.find('400 Bad Request') == -1 and res.text.find("class=\"c_table_style5\"")>-1:
                bl = False
            # print('请求得到的文本数据:'+res.text)
            elif (res.text.find('400 Bad Request') > -1):
                print('出现了400错误')
                raise Exception
            else:
                print("返回了未知的页面内容")
                print(res.text)
                raise Exception
        except Exception:
            print('出现了错误，开始更换代理')
            # proxies = {"http": requests.get('http://localhost:5010/get').text}
            # requests.get("http://localhost:5010/delete/?proxy={}".format(proxy))
            # proxy = requests.get('http://localhost:5010/get').text
            # proxies['http'] = proxy
            time.sleep(1)
    ret = [];
    if (res.text):
        print('开始解析爬行到的html数据' + str(res.content))
        soup = BeautifulSoup(res.content, 'lxml')
        trs = soup.find("table",class_="c_table_style5").find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            ret.append(tds[1].span.get_text())
            if(len(tds)==4):
                ret.append(tds[3].span.get_text())
    print(ret)
    return ret


if __name__ == '__main__':
    logging.basicConfig(filename='mf1.log', level=logging.INFO)
    getMainHTML(target=targets[1],mf_tpe="年检结果公告")