from django.http import HttpResponse
from openpyxl import Workbook
import xlsxwriter
from email.mime.base import MIMEBase
from email import encoders
from django.core.mail import EmailMultiAlternatives

def generate_by_openpyxl(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "PSC Stocks"
    headers = [
        "Id", "Product Code", "Variant Code", "Location",
        "Stock", "Updated Date", "Reserved", "Reserved date",
        "Location product code", "Due date", "Discontinued",
        "Est due date txt", "Est due date", "Pre order",
        "Pre order quantity", "External ref", "SAP ID"
    ]
    ws.append(headers)

    psc_stocks = ["get_queryset()"]
    for stock in psc_stocks:
        ws.append([
            stock.id, stock.product_code, stock.variant_code,
            stock.location_desc, stock.stock, str(stock.stock_updated_date),
            stock.reserved, str(stock.reserved_date),
            stock.location_product_code, str(stock.due_date),
            stock.is_discontinued, stock.est_due_date_txt,
            str(stock.est_due_date), stock.pre_order,
            stock.pre_order_quantity, stock.external_ref, stock.sap_id,
        ])
    wb.save('psc_stocks.xlsx')

def email_xlsx(request):
    msg = EmailMultiAlternatives("Newly Generated Excel File Check", f"This is your Newly generated excel File for", to=[request.user.email, 'mehedi.arbree@gmail.com'])
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open('my_data.xlsx', "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="my_data.xlsx"')
    msg.attach(part)
    msg.send(fail_silently=False)

def generate_by_xlsxwriter(request):
    workbook = xlsxwriter.Workbook('psc_stocks.xlsx')
    worksheet = workbook.add_worksheet("PSC Stocks")
    bold = workbook.add_format({'bold': True,})
    head = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'B2BEB5'
        })
    dat = workbook.add_format({
        'bold': 0,
        'align': 'left',
        'valign': 'vcenter'
        })
    worksheet.set_column('B:C', 15)
    worksheet.set_column('D:Z', 25)
    worksheet.set_row(0, 25)
    headers = [
        "Id", "Product Code", "Variant Code", "Location",
        "Stock", "Updated Date", "Reserved", "Reserved date",
        "Location product code", "Due date", "Discontinued",
        "Est due date txt", "Est due date", "Pre order",
        "Pre order quantity", "External ref", "SAP ID"
    ]
    values_field = [
        "id", "product_code", "variant_code", "location_desc", "stock",
        "stock_updated_date", "reserved", "reserved_date", "location_product_code", "due_date",
        "is_discontinued", "est_due_date_txt", "est_due_date", "pre_order", "pre_order_quantity",
        "external_ref", "sap_id"
    ]
    for index, head in enumerate(headers):
        worksheet.write(0, index, head, bold)
    # worksheet.merge_range(first_row=0, first_col=1, last_row=0, last_col=2, data='Campaign Name', cell_format=dat)
    psc_stocks = ["get_queryset()"]
    row = 1
    for stock in psc_stocks:
        for index, field in enumerate(values_field):
            worksheet.write(row, index, str(getattr(stock, field)), dat)
        row += 1
    workbook.close()


def download_excel(request):
    generate_by_xlsxwriter(request)
    response=HttpResponse(open('psc_stocks.xlsx', "rb").read(), content_type="application/xlsx")
    content="inline; filename=psc_stocks.xlsx"
    response['Content-Disposition']=content
    return response
