<<<<<<< HEAD
import requests
from  bs4 import BeautifulSoup
import random
headers = [{"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"},
=======
from bs4 import BeautifulSoup

import  requests
import  random
import time
target="https://r.gnavi.co.jp/jrt8sd4a0000/"
ugs = [{"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"},
>>>>>>> origin/master
           {
               "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
           {
               "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
           {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"},
           {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"},
           {
               "User-Agent": "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}]
<<<<<<< HEAD
if __name__ == '__main__':
    res = requests.get("https://r.gnavi.co.jp/jrt8sd4a0000/", params=None, headers=random.sample(headers, 1)[0]);
    # cookie=res.cookies;
    print(res.text)
    soup = BeautifulSoup(res.content, 'lxml')
=======
otherUrls=["https://r.gnavi.co.jp/area/areal2141/izakaya/rs/","https://r.gnavi.co.jp/area/aream2145/izakaya/rs/","https://r.gnavi.co.jp/area/aream2941/izakaya/rs/","https://r.gnavi.co.jp/area/jp/rs/?fwr=%E6%B5%B7%E8%88%9F&fw=%E6%B5%B7%E8%88%9F&redf=1"]
if __name__ == '__main__':





    i=1;
    while(1==1):
        proxy = requests.get('http://localhost:5010/get').text
        proxies = {"https": proxy}
        ug = random.sample(ugs, 1)[0];
        userAgent = ug['User-Agent']
        otherUrl = random.sample(otherUrls, 1)[0]
        header = {"Referer": otherUrl, "User-Agent": userAgent, "Host": "r.gnavi.co.jp"}

        try:
            res = requests.get("https://r.gnavi.co.jp",headers = header,timeout=5)
            cookie = res.cookies
            # ra=random.randint(1,10)
            # if(ra%2==0):
            res=requests.get(otherUrl,params=None,headers=header,cookies=cookie,timeout=10)
            if(res.status_code==200):
                print("访问前置url成功")
            time.sleep(random.randint(1,8))
            res=requests.get(target,params=None,headers=header,cookies=cookie,timeout=10)
            if(res.status_code==200):
                print("访问目标URL成功")
                print(res.content.decode())
            else:
                print("访问目标URL失败")
                print(str(res.status_code))
                print(res.content.decode())
            # else:
            time.sleep(random.randint(1,10))

            if(i%100==0):
                j=random.randint(30, 50)
                time.sleep(j)
                print("开始休息 %d 秒"%(j))
            i+=1
        except Exception :
            print("发生错误，更换代理")
            requests.get("http://localhost:5010/delete/?proxy={}".format(proxy))
            proxy = requests.get('http://localhost:5010/get').text
            proxies['https'] = proxy
            time.sleep(1)
>>>>>>> origin/master
