import xlrd
from db_kit import INOCC
import db_kit

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

def RAndWByRow(file,bRow,eRow,insurance):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)
    obj=None
    fCode=''
    fName='';
    sCode=''
    for i in range(bRow, eRow):
        if(sheet.cell(i,0).value!=''):
            fCode=str(int(sheet.cell(i,0).value))
            fName=str(sheet.cell(i,1).value)
            obj=INOCC()
            obj.code=fCode
            obj.name=fName
            obj.insurance=insurance
            db_kit.insert(obj)
            printObj(obj)
        if(sheet.cell(i,2).value!=''):
            sCode = str(int(sheet.cell( i,2).value))
            sName = str(sheet.cell( i,3).value)
            obj = INOCC()
            obj.pCode=fCode
            obj.code = sCode
            obj.name = sName
            obj.insurance = insurance
            db_kit.insert(obj)
            printObj(obj)
        if (sheet.cell( i,4).value != ''):
            tData=str(sheet.cell( i,4).value)
            ta=tData.split("、")
            for j in range(0,len(ta)):
                tCode=sCode+str(j).zfill(2)
                tName=ta[j]
                obj=INOCC()
                obj.name=tName
                obj.code=tCode
                obj.insurance=insurance
                obj.pCode=sCode
                obj.type=int(sheet.cell(i,5).value) if str(sheet.cell(i,5).value).strip()!='' else ''
                db_kit.insert(obj)
                printObj(obj)




def printObj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))



if __name__ == '__main__':


    # RAndWXls('/Users/yuhaihui/Documents/wh/人保财产.xls',2,679,699,'iorbcc',False)
    RAndWByRow('/Users/yuhaihui/Documents/wh/人保健康职业类别表.xlsx',150,325,'iorbjk')
