import xlrd
from db_kit import INOCC
import db_kit

def RAndWXls(file,col,bRow,eRow,insurance,hasCode=True):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)





    obj = INOCC()
    fCode=''
    if hasCode:
        f = sheet.cell(bRow, col - 4).value
        obj.insurance = insurance
        obj.name = f
        obj.code=sheet.cell(bRow,col-5).value
        fCode=obj.code
    else:
        f = sheet.cell(bRow, col - 2).value
        obj.insurance = insurance
        obj.name = f
        obj.code = f

    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

    db_kit.insert(obj)


    g=''
    gCode='';
    for i in range(bRow,eRow):
        obj=INOCC()

        if sheet.cell(i,col-2).value!='':
            g=sheet.cell(i,col-2).value
            if hasCode :
                obj.insurance = insurance
                obj.name = g
                obj.pCode=fCode
                obj.code = sheet.cell(i, col - 3).value
                gCode=obj.code
            else:
                obj.insurance = insurance
                obj.name = g
                obj.pCode = fCode
                obj.code = g
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
            obj.code = sheet.cell(i, col).value
            obj.name = sheet.cell(i, col ).value
            if sheet.cell(i, col + 1).ctype==2:
                obj.type = int(sheet.cell(i, col + 1).value)
            else:
                obj.type = str(sheet.cell(i, col + 1).value)

        obj.insurance=insurance


        print ('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))
        db_kit.insert(obj)



if __name__ == '__main__':


    RAndWXls('/Users/yuhaihui8913/Documents/wh/华泰职业类别表.xls',5,987,998,'ioht',True)