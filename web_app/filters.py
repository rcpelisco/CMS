from datetime import datetime
from dateutil.relativedelta import relativedelta

def format_datetime(value):
    datetime_object = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return datetime_object.strftime('%B %d, %Y - %I:%M:%S %p')

def format_date(value):
    date_object = datetime.strptime(value, '%Y-%m-%d')
    return date_object.strftime('%B %d, %Y')

def format_age(value):
    dob = datetime.strptime(value, '%Y-%m-%d')
    today = datetime.today()
    age = relativedelta(today, dob)
    return age.years
