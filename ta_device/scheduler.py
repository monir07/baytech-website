from django.utils.timezone import now
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth import get_user_model
User = get_user_model()


def get_data_from_device():
    print("get_data_from device scheduler running at {}".format(now()))


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(get_data_from_device, 'cron', hour=11, minute=9, second=00)
    scheduler.add_job(get_data_from_device, 'interval', minutes=2)
    scheduler.start()