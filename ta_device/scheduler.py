from django.utils.timezone import now
from apscheduler.schedulers.background import BackgroundScheduler
from zk import ZK, const
from django.contrib.auth import get_user_model
User = get_user_model()
from ta_device.models import Attendance as TaAttendance, Employee, TADevice


ip_list = [
    '172.16.26.20',
]
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
            
            att_obj = TaAttendance()
            for item in attendances:
                emp_obj = Employee.objects.filter(device_id_no=item.user_id).first()
                dev_obj = TADevice.objects.filter(ip_address='172.16.26.20').first()
                print('user id:{}, time:{}, status:{}, punch:{}'.format(item.user_id, item.timestamp, item.status, item.punch) )
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
            if conn:
                conn.disconnect()
    print("1. get_data_from device scheduler running at {}".format(now()))


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(get_data_from_device, 'cron', hour=11, minute=9, second=00)
    scheduler.add_job(get_data_from_device, 'interval', minutes=1)
    scheduler.start()