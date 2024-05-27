from django.core.management import BaseCommand
from django.utils.timezone import now
from apscheduler.schedulers.background import BackgroundScheduler
from zk import ZK, const
from django.contrib.auth import get_user_model
User = get_user_model()
from ta_device.models import Attendance as TaAttendance, Employee, TADevice
from base.helpers.func import (get_duration)


ip_list = [
    '172.16.26.20',
    '172.16.26.21',
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Getting Attendance......')
        get_data_from_device()
        print('All Data Migrations Success')


def get_data_from_device():
    for ip_addr in ip_list:
        print ("**************** Device IP: ", ip_addr, " ****************")
        zk = ZK(ip_addr, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        try:
            # connect to device
            conn = zk.connect()
            print ("Conncection Success.")
            conn.enable_device()
            print ("Device Enable.")
            attendances = conn.get_attendance()
            print('get attendnace: ', attendances)
            att_obj = TaAttendance()
            for item in attendances:
                print('user id:{}, time:{}, status:{}, punch:{}'.format(item.user_id, item.timestamp.time(), item.status, item.punch))
                dev_obj = TADevice.objects.get(ip_address=ip_addr)
                emp_obj = Employee.objects.get(device_id_no=item.user_id, device=dev_obj)
                try:
                    att_obj = TaAttendance.objects.get(emp=emp_obj, punch_in_date=item.timestamp)
                    print('---- Attendane Created Already ---')
                    att_obj.punch_out_device=dev_obj
                    att_obj.punch_out_date=item.timestamp
                    att_obj.punch_out_time=item.timestamp
                    att_obj.duration=str(get_duration(item.timestamp.time(), att_obj.punch_in_time))
                    att_obj.updated_by=User.objects.get(id='1')
                    att_obj.save()
                except TaAttendance.DoesNotExist:
                    TaAttendance.objects.create(
                    emp = emp_obj,
                    punch_in_device = dev_obj,
                    punch_in_date = item.timestamp,
                    punch_in_time = item.timestamp,
                    created_by = User.objects.get(id='1'),
                    )
            conn.clear_attendance()
            print ("Attendance Data Cleared.")
            
        except Exception as e:
            print ("Process terminate : {}".format(e))
        finally:
            pass
            if conn:
                conn.disconnect()
    # print("1. get_data_from device scheduler running at {}".format(now()))