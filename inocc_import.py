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
    soup = BeautifulSoup(open('/Users/yuhaihui8913/Documents/wh/太平洋人寿.html'))
    print(soup.prettify())


def printObj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))



if __name__ == '__main__':


    # RAndWXls('/Users/yuhaihui/Documents/wh/人保财产.xls',2,679,699,'iorbcc',False)
    # RAndWPACC('/Users/yuhaihui8913/Documents/wh/太平洋财产.xls',1,868,'iotpycc')
    # RAndWPAYL('/Users/yuhaihui8913/Documents/wh/职业类别表(平安).xls',2,1223,'iopayl')
    RAndWTPYRS_html()
