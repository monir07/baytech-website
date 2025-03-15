import random
from django.db import connection
from email.mime.base import MIMEBase
from email import encoders
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def send_simple_email(subject, body, to_mails: list, html_body: str = None):
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.FROM_EMAIL,
        to=to_mails
    )
    if html_body:
        email.attach_alternative(html_body, "text/html")  # Attach HTML version
    email.send()

def identifier_builder(table_name: str, prefix: str = None) -> str:
    with connection.cursor() as cur:
        query = f'SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1;'
        cur.execute(query)
        row = cur.fetchone()
    try:
        seq_id = str(row[0] + 1)
    except:
        seq_id = "1"
    random_suffix = random.randint(10, 99)
    if not prefix:
        return seq_id.rjust(8, '0') 
    return prefix + seq_id.rjust(8, '0') 


def send_mail_pdf(subject=None, to=None, text_content=None, pdf_content=None):
    from_email = settings.FROM_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,])
    if pdf_content:
        msg.attach_alternative(pdf_content, "application/pdf")
    msg.send(fail_silently=True)


def send_mail_with_attachment(subject=None,  text_content=None, to=None, file_link=None, ):
    msg = EmailMultiAlternatives(subject, text_content, to=[to,])
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(file_link, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="my_data.xlsx"')
    msg.attach(part)
    msg.send(fail_silently=False)


def make_file_response(file_link=None):
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(file_link, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="my_data.xlsx"')
    if part:
        response=HttpResponse(open('my_data.xlsx', "rb").read(), content_type="application/xlsx")
        content="inline; filename=my_data.xlsx"
        response['Content-Disposition']=content
        return response
