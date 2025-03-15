import re
import time
import random
import string
import qrcode
import base64
from typing import List, Callable
import uuid
import datetime
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Lookup
from django.apps import apps
from datetime import datetime, date, timedelta


def create_slug(title: str, random_str: str = None) -> str:
    title = re.sub('[^A-Za-z ]+', ' ', title).lower().strip()
    title = re.sub(' +', '-', title)
    if random_str:
        return title + '-' + random_str
    return title


def entries_to_remove(data: dict, removeable_keys: tuple) -> dict:
    for k in removeable_keys:
        data.pop(k, None)
    return data


def remove_duplicate_from_list(iterable: List, key:  Callable = None) -> List:
    if key is None:
        def key(x): return x

    seen = set()
    for elem in iterable:
        k = key(elem)
        if k in seen:
            continue

        yield elem
        seen.add(k)


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-", "")
    return random[0:string_length]


def convert_to_date(type: str, number: int) -> str:
    today = datetime.date.today()
    if type == "day":
        output_date = today + datetime.timedelta(days=number)
    elif type == "month":
        output_date = today + datetime.timedelta(days=number*30)
    elif type == "year":
        output_date = today + datetime.timedelta(days=number*365)
    return output_date

""" 
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None
"""

def unique_id_generate(number_of_id):
    unique_id_list = []
    for i in range(number_of_id):
        time_span = format(time.time(), '.14f')
        time_span = time_span.split('.')[1]
        unique_id_list.append(time_span)
        time.sleep(0.2)
    return unique_id_list


def format_filter_string(old_dict, keys):
    filtered_dict = {}
    for k in keys:
        if old_dict.get(k):
            filtered_dict[k] = old_dict.get(k)
    return filtered_dict


def get_model_from_any_app(model_name):
    for app_config in apps.get_app_configs():
        try:
            model = app_config.get_model(model_name)
            return model
        except LookupError:
            pass


def flatten(l_data):
    return [item for sublist in l_data for item in sublist]


def format_search_string(fields, keyword):
    Qr = None
    for field in fields:
        q = Q(**{"%s__icontains" % field: keyword })
        if Qr:
            Qr = Qr | q
        else:
            Qr = q
    return Qr


def format_filter_string(old_dict,keys):
    filtered_dict = {}
    for k in keys:
        if old_dict.get(k):
            filtered_dict[k] = old_dict.get(k)
    return filtered_dict

def snake_to_title(string: str):
    return string.replace("_", " ").title()

def find_common_groups(user_groups, target_groups):
    return list(set(user_groups) & set(target_groups))

def password_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params

def get_fields(model, fieldnames):
    return [model._meta.get_field(field) for field in fieldnames]

class Breadcrumb:
    def __init__(self, name, url=None):
        self.name = name
        self.url = url


def get_duration(start_time, end_time):
        # Combine start_time and end_time with today's date
        today = date.today()
        start_datetime = datetime.combine(today, start_time)
        end_datetime = datetime.combine(today, end_time)

        # Calculate the duration
        duration = end_datetime - start_datetime

        # Handle cases where end_time might be the next day
        if duration < timedelta(0):
            duration += timedelta(days=1)

        # Return the duration in your preferred format
        return duration


# Generate Qr code from web link.
def generate_qr_code(url_link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=4,
    )
    qr.add_data(url_link)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to a base64 string
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_image = base64.b64encode(buffer.getvalue()).decode()
    return qr_code_image