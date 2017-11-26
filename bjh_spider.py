#
#   爬行保监会
#
#   target:http://www.circ.gov.cn/tabid/2576/Default.aspx
#


import requests
from bs4 import BeautifulSoup
import re
import xlsxwriter
import datetime
import time
import random
import db_kit
import logging

domain = 'http://www.circ.gov.cn/'
target = 'http://www.circ.gov.cn/tabid/2576/Default.aspx'
headers = [{"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"},
           {
               "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
           {
               "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
           {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"},
           {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"},
           {
               "User-Agent": "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}]


def getMainHTML():
    session=requests.session()
    res = session.get(target, params=None, headers=random.sample(headers, 1)[0]);
    cookie=res.cookies;
    soup = BeautifulSoup(res.content, 'lxml')
    div_a = soup.find(id='ess_contentpane').find_all('a', recursive=False)
    # div_a=div_a.find_next_siblings('a')
    bxgslx = ''
    for a in div_a:
        '''
            设置特殊查询的区域
        '''
        if a['name'] !='8245':continue
        pageTotal = soup.find(id='ess_ctr' + a['name'] + '_OrganizationList_lblPageNum').get_text();
        pageNum = soup.find(id='ess_ctr' + a['name'] + '_OrganizationList_lblAtPageNum').get_text();
        pageTotal = int(pageTotal if pageTotal else '1')
        pageNum = int(pageNum if pageNum else '1')
        bxgslx = soup.find(id='ess_ctr' + a['name'] + '_OrganizationList_lblClassName')
        print('当前页 %d ,一共 %d 页' % (pageNum, pageTotal))
        __VIEWSTATE = ''
        __VIEWSTATEGENERATOR = ''
        for i in range(0, pageTotal+1):
            logging.info('编号为 %s 的项目 执行了第 %d 次 ' % (a['name'], i))
            print('编号为 %s 的项目 执行了第 %d 次 ' % (a['name'], i))
            urls = []
            p = {}
            header = {}


            if (i == 0):
                urls = soup.find(id='ess_ctr' + a['name'] + '_OrganizationList_rptCompany').find_all('a')
                __VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
                __VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']


            else:

                p = {
                    "__EVENTTARGET": (None, "ess$ctr" + a['name'] + "$OrganizationList$lbnToPage",None,),
                    "ess$ctr" + a['name'] + "$OrganizationList$lblAtPageNum": (None, str(i+1)),
                    "__EVENTARGUMENT": (None, ""),
                    # "ess$ctr8245$OrganizationList$lblAtPageNum": (None, ""),
                    "__VIEWSTATEGENERATOR": (None, __VIEWSTATEGENERATOR),
                    # "ess$ctr8247$OrganizationList$lblAtPageNum": (None, "")
                    # , "ess$ctr8248$OrganizationList$lblAtPageNum": (None, ""),
                    # "ess$ctr8249$OrganizationList$lblAtPageNum": (None, ""),
                    # "ess$ctr8250$OrganizationList$lblAtPageNum": (None, ""),
                    # "__essVariable": (None, ""),
                    # "ScrollTop": (None, ""),
                    # "select": (None, ""),
                    # "select2": (None, ""),
                    # "q": (None, ""),
                    "__VIEWSTATE": (None, __VIEWSTATE)}

                header = random.sample(headers, 1)[0];
                header=header['User-Agent']

                proxy = requests.get('http://192.168.50.229:5010/get').text
                proxies = {"http": proxy}
                _res = session.post(target,
                                     files=p,cookies=cookie,
                                    # proxies=proxies,
                                     headers={
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Referer": "http://www.circ.gov.cn/tabid/2576/Default.aspx",
                        "Host": "www.circ.gov.cn",
                        "Accept-Language": "zh-CN,zh;q = 0.9",
                        "Origin": "http://www.circ.gov.cn",
                        # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryl8pqZs1k7pDwvrlo",
                        "User-Agent": header})
                # print('分页请求参数')
                # print(_res.request.body.decode())
                # print(_res.request.headers)
                # print(_res.content.decode())
                _soup = BeautifulSoup(_res.content, 'lxml')
                urls = _soup.find(id='ess_ctr' + a['name'] + '_OrganizationList_rptCompany')
                # print(_res.text)
                if  urls is not None:
                    urls=urls.find_all('a')
                else:
                    logging.error('编号为 %s 的项目 执行了第 %d 次 ' % (a['name'], i)+",主页没有解析到正确的链接数据")
                    continue
                __VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
                __VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
            print(urls)
            companyInfo = None
            insurer = None
            # companyInfos=[];
            for url in urls:
                detailUrl = re.findall(r"'(.+?)'", str(url['onclick']));
                ret = db_kit.findOnByUrl(detailUrl[0])
                if (ret is None):
                    companyInfo = getCompanyHtml(detailUrl[0])
                    if (companyInfo.__len__() == 9):
                        insurer = db_kit.Insurer()
                        insurer.orgName = companyInfo[0]
                        insurer.orgType = companyInfo[1]
                        insurer.cat = companyInfo[2]
                        insurer.orgAddress = companyInfo[3]
                        insurer.tel = companyInfo[4]
                        insurer.leader = companyInfo[5]
                        insurer.capital = companyInfo[6]
                        insurer.registerAddress = companyInfo[7]
                        insurer.state = companyInfo[8]
                        insurer.url = detailUrl[0]
                        insurer.catalog = bxgslx.get_text()
                        db_kit.insert(insurer)
                    else:
                        logging.error(detailUrl[0] + '返回的内容不正确。没有解析出正确内容')
                # companyInfos.append(companyInfo)
                    time.sleep(random.randint(1, 2))
                # writeExcel(bxgslx.string,companyInfos)


def getCompanyHtml(url):
    proxy = requests.get('http://192.168.50.229:5010/get').text
    proxies = {"http": proxy}
    bl = True
    res = None;
    while (bl):
        print('爬行的URL>>' + domain + url)
        print('使用的代理为>>' + str(proxies))
        try:
            res = requests.get(domain + url, params=None, headers=random.sample(headers, 1)[0], proxies=proxies, timeout=8)
            if res.status_code==200 and res.text != '' and res.text.find('400 Bad Request') == -1 and res.text.find("class=\"TableHeader1\"")>-1:
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
            requests.get("http://192.168.50.229:5010/delete/?proxy={}".format(proxy))
            proxy = requests.get('http://192.168.50.229:5010/get').text
            proxies['http'] = proxy

    ret = [];
    if (res.text):
        print('开始解析爬行到的html数据' + str(res.content))
        soup = BeautifulSoup(res.content, 'lxml')
        trs = soup.find_all(attrs={"bgcolor": "#FFFFFF"})
        for tr in trs:
            tds = tr.find_all("td")
            ret.append(tds[1].span.get_text())

    print(ret)
    return ret


def writeInsurerExcel(bxgslx, companyInfos=None):
    workbook = xlsxwriter.Workbook(bxgslx + '.xlsx')

    worksheet=createInsurerWS(workbook=workbook,name=bxgslx)

    # for i, ci in enumerate(companyInfos, 1):
    #     for j, c in enumerate(ci):
    #         worksheet.write(i, j, str(c))
    for i, ci in enumerate(companyInfos, 1):

        worksheet.write(i,0,ci.orgName)
        worksheet.write(i,1,ci.orgType)
        worksheet.write(i,2,ci.cat)
        worksheet.write(i,3,ci.orgAddress)
        worksheet.write(i,4,ci.tel)
        worksheet.write(i,5,ci.leader)
        worksheet.write(i,6,ci.capital)
        worksheet.write(i,7,ci.registerAddress)
        worksheet.write(i,8,ci.state)
        # if i%100==0:
        #     worksheet=createInsurerWS(workbook=workbook,name=bxgslx+str(i/100))
    workbook.close()
def createInsurerWS(workbook,name):
    bold = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet(name=name)
    worksheet.set_column('A:A', 20)
    worksheet.set_column('D:D', 25)
    worksheet.write('A1', '机构名称', bold)
    worksheet.write('B1', '机构类别', bold)
    worksheet.write('C1', '设立时间', bold)
    worksheet.write('D1', '机构地址', bold)
    worksheet.write('E1', '联系电话', bold)
    worksheet.write('F1', '负责人', bold)
    worksheet.write('G1', '中资外资', bold)
    worksheet.write('H1', '注册地', bold)
    worksheet.write('I1', '状态', bold)
    return worksheet

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO)
    # getMainHTML()
    ret=db_kit.findAll(db_kit.Insurer,"保险公司－人身险")
    print("查询记录数为 %d "%(len(ret)))
    writeInsurerExcel(bxgslx="保险公司－人身险",companyInfos=ret)


