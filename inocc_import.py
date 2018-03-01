import xlrd
from db_kit import INOCC
import db_kit
from bs4 import BeautifulSoup

def RAndWXls(file,col,bRow,eRow,insurance,hasCode=True):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(1)





    obj = INOCC()
    fCode=''
    if hasCode:
        f = sheet.cell(bRow, col - 4).value
        obj.insurance = insurance
        obj.name = f
        obj.code=sheet.cell(bRow,col-5).value
        fCode=obj.code
    else:
        f = str(sheet.cell(bRow, col - 2).value)
        obj.insurance = insurance
        fa=f.split(" ")
        obj.name = fa[-1]
        obj.code = fa[0]
        fCode=obj.code

    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

    db_kit.insert(obj)


    g=''
    gCode='';
    fl=''
    for i in range(bRow,eRow):
        obj=INOCC()

        if sheet.cell(i,col-1).value!='':
            fl=''
            g=str(sheet.cell(i,col-1).value)
            ga=g.split(" ")
            if hasCode :
                obj.insurance = insurance
                obj.name = g
                obj.pCode=fCode
                obj.code = sheet.cell(i, col - 3).value
                gCode=obj.code
            else:
                obj.insurance = insurance
                obj.name = ga[-1]
                obj.pCode = fCode
                obj.code = ga[0]
                gCode = obj.code
            db_kit.insert(obj)
            print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


        obj=INOCC()
        obj.pCode=gCode
        if hasCode:
            obj.code=sheet.cell(i,col-1).value
            obj.name=sheet.cell(i,col).value
            if sheet.cell(i,col+1).ctype==2:
                obj.type=int(sheet.cell(i,col+1).value)
            else:
                obj.type = str(sheet.cell(i, col + 1).value)
        else:
            d=str(sheet.cell(i, col).value)
            if d.startswith("注"):
                continue
            da=d.split(" ")
            if len(da) == 1 :
                fl=da[0]
                continue


            obj.code = da[0]
            obj.name = da[-1] if fl=='' else fl+'-'+da[-1]
            if sheet.cell(i, col + 1).ctype==2:
                obj.type = int(sheet.cell(i, col + 1).value)
            else:
                obj.type = str(sheet.cell(i, col + 1).value)

        obj.insurance=insurance


        print ('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))
        db_kit.insert(obj)

def RAndWPACC(file,bRow,eRow,insurance):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(2)
    obj=None
    fCode=''
    fName=''
    sCode=''
    header=''
    lastF=''
    for i in range(bRow, eRow):
        if(str(sheet.cell(i,0).value).strip()!=''):
            fCode=str(sheet.cell(i,0).value)
            if fCode!=lastF:
                header=''
            fName=str(sheet.cell(i,0).value)
            obj=INOCC()
            obj.code=fCode
            obj.name=fName
            obj.insurance=insurance
            if db_kit.existCheck(obj.code,insurance)=='no':
                db_kit.insert(obj)
                printObj(obj)
        if(str(sheet.cell(i,1).value).strip()!=''):
            sCode = str(sheet.cell( i,1).value)
            sName = str(sheet.cell( i,1).value)
            obj = INOCC()
            obj.pCode=fCode
            obj.code = sCode
            obj.name = sName
            obj.insurance = insurance
            if db_kit.existCheck(obj.code,insurance)=='no':
                db_kit.insert(obj)
                printObj(obj)
        if (str(sheet.cell( i,2).value).strip() != ''):

            obj=INOCC()
            obj.name=header+'-'+str(sheet.cell( i,3).value) if header!='' else str(sheet.cell( i,3).value)
            obj.name=obj.name.strip()
            obj.code=str(sheet.cell( i,2).value).strip()
            obj.insurance=insurance
            obj.pCode=sCode
            obj.type=int(sheet.cell(i,4).value) if str(sheet.cell(i,4).value).strip()!='' else ''
            db_kit.insert(obj)
            printObj(obj)
        elif str(sheet.cell( i,3).value).strip().startswith('注：'):
            continue
        else:
            header=str(sheet.cell( i,3).value)



        lastF=fCode


def RAndWPAYL(file,bRow,eRow,insurance):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(1)
    obj = None
    fCode = ''
    fName = ''
    sCode = ''
    header = ''
    lastF = ''
    for i in range(bRow, eRow):
        if (str(sheet.cell(i, 0).value).strip() != ''):
            fCode = str(sheet.cell(i, 0).value).strip()[0:2]
            fName = str(sheet.cell(i, 0).value).strip()[2:]
            if fCode!=lastF:
                header=''
            obj = INOCC()
            obj.code = fCode
            obj.name = fName
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if (str(sheet.cell(i, 1).value).strip() != ''):
            sCode = str(sheet.cell(i, 1).value).strip()[0:4]
            sName = str(sheet.cell(i, 1).value).strip()[4:]
            obj = INOCC()
            obj.pCode = fCode
            obj.code = sCode
            obj.name = sName
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if (str(sheet.cell(i, 2).value).strip() != ''):

            obj = INOCC()
            obj.name = header + '-' + str(sheet.cell(i, 3).value) if header != '' else str(sheet.cell(i, 3).value)
            obj.name = obj.name.strip()
            obj.code = str(sheet.cell(i, 2).value).strip()
            obj.insurance = insurance
            obj.pCode = sCode
            if sheet.cell(i,4).ctype==2:
                obj.type = int(sheet.cell(i, 4).value) if str(sheet.cell(i, 4).value).strip() != '' else ''
            else:
                obj.type = str(sheet.cell(i, 4).value)
            db_kit.insert(obj)
            printObj(obj)
        elif str(sheet.cell(i, 3).value).strip().startswith('注：'):
            continue
        else:
            header = str(sheet.cell(i, 3).value)

        lastF = fCode


def RAndWTPYRS_html():
    soup = BeautifulSoup(open('/Users/yuhaihui8913/Documents/wh/太平洋人寿final.html'))
    print(soup.prettify())
    trs = soup.find("table", class_="MsoNormalTable").find_all("tr")
    obj = None
    fCode = ''
    fName = ''
    sCode = ''
    header = ''
    lastF = ''
    for tr in trs:
        tds = tr.find_all("td")

        if len(tds)==5:
           if True:
               ps=tds[0].find_all('p')
               fCode = str(ps[0].get_text()).strip() if str(ps[0].get_text()).strip()!='' else fCode  if len(ps)==1 else ps[0].get_text()
               fName = str(ps[0].get_text()).strip() if str(ps[0].get_text()).strip()!='' else fCode if len(ps)==1 else ps[1].get_text()
               if fCode != lastF:
                   header = ''
               obj = INOCC()
               obj.code = fCode
               obj.name = fName
               obj.insurance = 'iotpyrs'
               if db_kit.existCheck(obj.code, 'iotpyrs') == 'no':
                    db_kit.insert(obj)
                    printObj(obj)
           if True:
               ps = tds[1].find_all('p')
               sCode = str(ps[0].get_text()).strip() if len(ps)==1 else str(ps[0].get_text()).strip()
               sName = str(ps[0].get_text()).strip() if len(ps)==1 else str(ps[1].get_text()).strip()
               obj = INOCC()
               obj.pCode = fCode
               obj.code = sCode
               obj.name = sName
               obj.insurance = 'iotpyrs'
               if db_kit.existCheck(obj.code, 'iotpyrs') == 'no':
                    db_kit.insert(obj)
                    printObj(obj)
           if True:

               obj = INOCC()
               spans=tds[2].p.contents
               obj.name = header + '-' + str(tds[2].p.contents[1].get_text()).strip() if header != '' else str(tds[2].p.contents[1].get_text()).strip()
               obj.name = obj.name.strip()
               obj.code = tds[2].p.contents[0].get_text().strip()
               obj.insurance = 'iotpyrs'
               obj.pCode = sCode
               obj.type = tds[4].p.span.get_text().strip()
               db_kit.insert(obj)
               printObj(obj)
        if len(tds)==4:
           if True:
               ps=tds[0].find_all('p')
               sCode = str(ps[0].get_text()).strip()
               sName = str(ps[1].get_text()).strip()
               obj = INOCC()
               obj.pCode = fCode
               obj.code = sCode
               obj.name = sName
               obj.insurance = 'iotpyrs'
               if db_kit.existCheck(obj.code, 'iotpyrs') == 'no':
                    db_kit.insert(obj)
                    printObj(obj)
           if True:
               obj = INOCC()
               obj.name = header + '-' + str(tds[1].p.contents[1].get_text().strip()) if header != '' else str(tds[1].p.contents[1].get_text()).strip()
               obj.name = obj.name.strip()
               obj.code = tds[1].p.contents[0].get_text().strip()
               obj.insurance = 'iotpyrs'
               obj.pCode = sCode
               obj.type = tds[3].p.span.get_text().strip()
               db_kit.insert(obj)
               printObj(obj)
        if len(tds)==3:
           if True:
               obj = INOCC()
               obj.name = header + '-' + str(tds[0].p.contents[1].get_text()).strip() if header != '' else str(tds[0].p.contents[1].get_text()).strip()
               obj.name = obj.name.strip()
               obj.code = tds[0].p.contents[0].get_text().strip()
               obj.insurance = 'iotpyrs'
               obj.pCode = sCode
               try:
                   obj.type = tds[2].get_text().strip()
               except AttributeError :
                   print(tds[2]+'===========================================================================')


               db_kit.insert(obj)
               printObj(obj)
        if len(tds)==2:
            ps = tds[0].find_all('p')
            if len(ps)==2:
                sCode = str(ps[0].get_text()).strip()
                sName = str(ps[1].get_text()).strip()
                obj = INOCC()
                obj.pCode = fCode
                obj.code = sCode
                obj.name = sName
                obj.insurance = 'iotpyrs'
                if db_kit.existCheck(obj.code, 'iotpyrs') == 'no':
                    db_kit.insert(obj)
                    printObj(obj)
            if tds[1].p.span.get_text().strip() != '':
               header=tds[1].p.span.get_text().strip()
        if len(tds)==1:
           if tds[0].p.span.get_text().strip() != '' and not str(tds[0].p.span.get_text()).strip().startswith('注：'):
               header=tds[0].p.span.get_text().strip()
           else:
               continue
    lastF = fCode


def WAndRAxcc():
    workbook = xlrd.open_workbook('/Users/yuhaihui8913/Documents/wh/安心财产职业类别表.xlsx')
    sheet = workbook.sheet_by_index(0)
    obj = None
    fCode = ''
    fName = ''
    sCode = ''
    header = ''
    lastF = ''
    insurance='ioaxcc'
    for i in range(5, 686):
        if (str(sheet.cell(i, 5).value).strip() != ''):
            fCode = str(sheet.cell(i, 5).value).strip()
            fName = str(sheet.cell(i, 5).value).strip()
            if fCode != lastF:
                header = ''
            obj = INOCC()
            obj.code = fCode
            obj.name = fName
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if (str(sheet.cell(i, 6).value).strip() != ''):
            sCode = str(sheet.cell(i, 6).value).strip()
            sName = str(sheet.cell(i, 6).value).strip()
            obj = INOCC()
            obj.pCode = fCode
            obj.code = sCode
            obj.name = sName
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if (str(sheet.cell(i, 7).value).strip() != ''):

            obj = INOCC()
            obj.name = header + '-' + str(sheet.cell(i, 7).value) if header != '' else str(sheet.cell(i, 7).value)
            obj.name = obj.name.strip()
            obj.code = obj.name
            obj.insurance = insurance
            obj.pCode = sCode
            if sheet.cell(i, 8).ctype == 2:
                obj.type = int(sheet.cell(i, 8).value) if str(sheet.cell(i, 8).value).strip() != '' else ''
            else:
                obj.type = str(sheet.cell(i, 8).value).strip()
            db_kit.insert(obj)
            printObj(obj)
        elif str(sheet.cell(i, 7).value).strip().startswith('注：'):
            continue
        else:
            header = str(sheet.cell(i, 7).value)

        lastF = fCode

def WAndRHt():
    workbook = xlrd.open_workbook('/Users/yuhaihui8913/Documents/wh/华泰职业类别表.xls')
    sheet = workbook.sheet_by_index(0)
    obj = None
    fCode = ''
    fName = ''
    sCode = ''
    header = ''
    lastF = ''
    insurance='ioht'
    for i in range(2, 998):
        if (str(sheet.cell(i, 0).value).strip() != ''):
            fCode = str(sheet.cell(i, 0).value).strip()
            fName = (str(sheet.cell(i, 1).value).strip())[2:]
            if fCode != lastF:
                header = ''
            obj = INOCC()
            obj.code = fCode
            obj.name = fName
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if (str(sheet.cell(i, 2).value).strip() != ''):
            sCode = str(sheet.cell(i, 2).value).strip()
            sName = (str(sheet.cell(i, 3).value).strip())[4:]
            obj = INOCC()
            obj.pCode = fCode
            obj.code = sCode
            obj.name = sName
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if (str(sheet.cell(i, 4).value).strip() != ''):

            obj = INOCC()
            obj.name = header + '-' + str(sheet.cell(i, 5).value) if header != '' else str(sheet.cell(i, 5).value)
            obj.name = obj.name.strip()
            obj.code = str(sheet.cell(i, 4).value).strip()
            obj.insurance = insurance
            obj.pCode = sCode
            if sheet.cell(i, 6).ctype == 2:
                obj.type = int(sheet.cell(i, 6).value) if str(sheet.cell(i, 6).value).strip() != '' else ''
            else:
                obj.type = str(sheet.cell(i, 6).value).strip()
            db_kit.insert(obj)
            printObj(obj)
        elif str(sheet.cell(i, 5).value).strip().startswith('注：'):
            continue
        else:
            header = str(sheet.cell(i, 5).value)

        lastF = fCode

def WAndRRbcc():
    workbook = xlrd.open_workbook('/Users/yuhaihui8913/Documents/wh/人保财产.xls')
    sheet = workbook.sheet_by_index(1)
    obj = None
    fCode = ''
    fName = ''
    sCode = ''
    header = ''
    lastF = ''
    insurance='iorbcc'
    for i in range(1, 699):
        if (str(sheet.cell(i, 0).value).strip() != ''):
            fCode = (str(sheet.cell(i, 0).value).strip())[0:2]
            fName = (str(sheet.cell(i, 0).value).strip())[2:]
            if fCode != lastF:
                header = ''
            obj = INOCC()
            obj.code = fCode.replace(' ','')
            obj.name = fName.replace(' ','')
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if (str(sheet.cell(i, 1).value).strip() != ''):
            sCode = (str(sheet.cell(i, 1).value).strip())[0:4]
            sName = (str(sheet.cell(i, 1).value).strip())[4:]
            obj = INOCC()
            obj.pCode = fCode
            obj.code = sCode.replace(' ','')
            obj.name = sName.replace(' ','')
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if (str(sheet.cell(i, 2).value).strip() != '' and (str(sheet.cell(i, 2).value).startswith('0') or str(sheet.cell(i, 2).value).startswith('1') or str(sheet.cell(i, 2).value).startswith('2'))):

            obj = INOCC()
            obj.name = header + '-' + (str(sheet.cell(i, 2).value).strip())[6:] if header != '' else (str(sheet.cell(i, 2).value).strip())[6:]
            obj.name = obj.name.replace(' ','')
            obj.code = (str(sheet.cell(i, 2).value).strip())[0:6]
            obj.code=obj.code.replace(' ','')
            obj.insurance = insurance
            obj.pCode = sCode
            if sheet.cell(i, 3).ctype == 2:
                obj.type = int(sheet.cell(i, 3).value) if str(sheet.cell(i, 3).value).strip() != '' else ''
            else:
                obj.type = str(sheet.cell(i, 3).value).strip()
            db_kit.insert(obj)
            printObj(obj)
        elif str(sheet.cell(i, 2).value).strip().startswith('注：'):
            continue
        else:
            header = str(sheet.cell(i, 2).value).strip()

        lastF = fCode
        print(str(i))
#人保健康
def WAndRRbjk():
    workbook = xlrd.open_workbook('/Users/yuhaihui8913/Documents/wh/人保健康职业类别表.xlsx')
    sheet = workbook.sheet_by_index(0)
    obj = None
    fCode = ''
    fName = ''
    sCode = ''
    header = ''
    lastF = ''
    insurance='iorbjk'
    for i in range(1, 325):
        if (str(sheet.cell(i, 0).value).strip() != ''):
            fCode = (int(sheet.cell(i, 0).value))
            fName = (str(sheet.cell(i, 1).value).strip())
            if fCode != lastF:
                header = ''
            obj = INOCC()
            obj.code = fCode
            obj.name = fName.replace(' ','')
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if (str(sheet.cell(i, 2).value).strip() != ''):
            sCode = (int(sheet.cell(i, 2).value))
            sName = (str(sheet.cell(i, 3).value).strip())
            obj = INOCC()
            obj.pCode = fCode
            obj.code = sCode
            obj.name = sName.replace(' ','')
            obj.insurance = insurance
            # if db_kit.existCheck(obj.code, insurance) == 'no':
            db_kit.insert(obj)
            printObj(obj)
        if str(sheet.cell(i, 4).value).strip() != '' :

            obj = INOCC()

            s=str(sheet.cell(i,4).value).replace(' ','')
            if s.startswith('ns'):
                obj.name = header + '-' + (str(sheet.cell(i, 4).value).strip()) if header != '' else (str(sheet.cell(i, 4).value).strip())
                obj.name = obj.name.replace(' ','')
                obj.code = str(sCode)+'00'
                obj.code=obj.code.replace(' ','')
                obj.insurance = insurance
                obj.pCode = sCode
                if sheet.cell(i, 5).ctype == 2:
                    obj.type = int(sheet.cell(i, 5).value) if str(sheet.cell(i, 5).value).strip() != '' else ''
                else:
                    obj.type = str(sheet.cell(i, 5).value).strip()
                db_kit.insert(obj)
            else:
                l=s.split('、')
                j=0;
                for tname in l:
                    obj = INOCC()
                    obj.name = header + '-' + tname if header != '' else tname
                    obj.name = obj.name.replace(' ', '')
                    obj.code = str(sCode) + str(j).zfill(2)
                    obj.code = obj.code.replace(' ', '')
                    obj.insurance = insurance
                    obj.pCode = sCode
                    if sheet.cell(i, 5).ctype == 2:
                        obj.type = int(sheet.cell(i, 5).value) if str(sheet.cell(i, 5).value).strip() != '' else ''
                    else:
                        obj.type = str(sheet.cell(i, 5).value).strip()
                    db_kit.insert(obj)
                    j+=1

        elif str(sheet.cell(i, 2).value).strip().startswith('注：'):
            continue
        else:
            header = str(sheet.cell(i, 2).value).strip()

        lastF = fCode
        print(str(i))

def printObj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))



if __name__ == '__main__':


    # RAndWXls('/Users/yuhaihui/Documents/wh/人保财产.xls',2,679,699,'iorbcc',False)
    # RAndWPACC('/Users/yuhaihui8913/Documents/wh/太平洋财产.xls',1,868,'iotpycc')
    # RAndWPAYL('/Users/yuhaihui8913/Documents/wh/职业类别表(平安).xls',2,1223,'iopayl')
    # RAndWTPYRS_html()
    # WAndRAxcc()
    # WAndRHt()
    # WAndRRbcc()
    WAndRRbjk()