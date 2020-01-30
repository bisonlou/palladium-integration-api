import datetime


def get_month_name(month_num):
    month = datetime.date(1900, month_num, 1).strftime('%B')
    print(month)
    return month
