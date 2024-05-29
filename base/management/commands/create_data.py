import csv
from django.core.management import BaseCommand
from django.utils.timezone import now
from apscheduler.schedulers.background import BackgroundScheduler
from zk import ZK, const
from django.contrib.auth import get_user_model
User = get_user_model()
from ta_device.models import Attendance as TaAttendance, Employee, TADevice
from base.helpers.func import (get_duration)


ip_list = [
    '172.16.26.21',
    '172.16.26.17',
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('..........Getting Data From Device......')
        get_user_data_from_device()
        print('.......... All Process Completed .........')


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
            # attendances = conn.get_attendance()
            attendances = conn.get_attendance()
            print('get attendnace: ', attendances)
            att_obj = TaAttendance()
            line_count = 0
            header_list = [["SL NO", "USER ID", "TIME", "DATE","STATUS", "PUNCH"]]
            for item in attendances:
                # print('user id:{}, time:{}, status:{}, punch:{}'.format(item.user_id, item.timestamp.time(), item.status, item.punch))
                line_count += 1
                header_list.append([line_count, item.user_id, item.timestamp.time(), item.timestamp, item.status, item.punch])
                """ 
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
                """
            with open(f'{ip_addr}_attendance_data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(header_list)
            # conn.clear_attendance()
            # print ("Attendance Data Cleared.")
            
        except Exception as e:
            print ("Process terminate : {}".format(e))
        finally:
            pass
            if conn:
                conn.disconnect()
        
    # print("1. get_data_from device scheduler running at {}".format(now()))


def get_user_data_from_device():
    for ip_addr in ip_list:
        print ("**************** Device IP: ", ip_addr, " ****************")
        zk = ZK(ip_addr, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        try:
            # connect to device
            conn = zk.connect()
            print ("Conncection Success.")
            conn.enable_device()
            print ("Device Enable.")
            all_users = conn.get_users()
            print('get users: ', len(all_users))
            line_count = 0
            header_list = [["sl", "name", "u id", "user id", "card no"]]
            for item in all_users:
                line_count += 1
                header_list.append([line_count, item.name, item.uid, item.user_id, item.card])
            with open(f'{ip_addr}_user_data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(header_list)
            
        except Exception as e:
            print ("Process terminate : {}".format(e))
        
    # print("1. get_data_from device scheduler running at {}".format(now()))


def get_finger_template_from_device():
    for ip_addr in ip_list:
        print ("**************** Device IP: ", ip_addr, " ****************")
        zk = ZK(ip_addr, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        try:
            # connect to device
            conn = zk.connect()
            print ("Conncection Success.")
            conn.enable_device()
            print ("Device Enable.")
            all_templates = conn.get_templates()
            print('get fingers: ', len(all_templates))
            line_count = 0
            header_list = [["SL NO", "u id", "f id", "template" , "mark"]]
            for item in all_templates:
                line_count += 1
                header_list.append([line_count, item.uid, item.fid, item.template, item.mark])
            with open(f'{ip_addr}_finger_data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(header_list)
        except Exception as e:
            print ("Process terminate : {}".format(e))