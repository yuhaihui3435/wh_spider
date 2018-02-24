
import xlsxwriter
import db_kit

def createWS(workbook,name):
    bold = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet(name=name)
    worksheet.set_column('A:A', 20)
    worksheet.set_column('D:D', 25)
    worksheet.set_column('K:K', 40)
    worksheet.write('A1', '企业名', bold)
    worksheet.write('B1', '登记时间', bold)
    worksheet.write('C1', '登记机构', bold)
    worksheet.write('D1', '统计机构代码证', bold)
    worksheet.write('E1', '法人', bold)
    worksheet.write('F1', '业务主管单位', bold)
    worksheet.write('G1', '证书有效期', bold)
    worksheet.write('H1', '地址', bold)
    worksheet.write('I1', '手机号', bold)
    worksheet.write('J1', '办公电话', bold)
    worksheet.write('K1', '业务范围', bold)
    return worksheet

if __name__ == '__main__':
    workbook = xlsxwriter.Workbook( '民非企业.xlsx')
    worksheet = createWS(workbook=workbook, name='民非企业')

    ret=db_kit.findMfAll()

    for index,r in enumerate(ret,1):
        worksheet.write(index,0,r.reg_name)
        worksheet.write(index,1,r.reg_time)
        worksheet.write(index,2,r.reg_org)
        worksheet.write(index,3,r.reg_num)
        worksheet.write(index,4,r.legal)
        worksheet.write(index,5,r.mng_unit)
        worksheet.write(index,6,r.expiry_date)
        worksheet.write(index,7,r.ads)
        worksheet.write(index,8,r.tel)
        worksheet.write(index,9,r.phone)
        worksheet.write(index,10,r.scope)

    workbook.close();



