from datetime import datetime, date, timedelta
from django.db import models
from django.db.models import UniqueConstraint
from base.models import BaseModel


class SimplifyBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


# Create your models here.
class TADevice(BaseModel):
    device_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100, unique=True)
    device_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
    
    def  __str__(self) -> str:
        return f'{self.device_name}:{self.ip_address}'


class DeviceControl(SimplifyBaseModel):
    device = models.ForeignKey(TADevice, on_delete=models.CASCADE, related_name='device_control')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) -> str:
        return f'{self.device}>{self.start_time}:{self.end_time}'
    
    class Meta:
        ordering = ('-created_at',)


class Department(SimplifyBaseModel):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        ordering=('-created_at', )


class Section(SimplifyBaseModel):
    department_list = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='selction_list')
    name = models.CharField(max_length=80, unique=True)

    def __str__(self) -> str:
        return f'{self.department_list.name}:{self.name}'
    
    class Meta:
        ordering=('-created_at', )


class Holiday(SimplifyBaseModel):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        ordering=('-created_at', )


class HolidayCalender(SimplifyBaseModel):
    holiday_list = models.ForeignKey(Holiday, on_delete=models.CASCADE, related_name='holiday_calender')
    date_from = models.DateField()
    date_to = models.DateField()
    total_day = models.DecimalField(max_digits=5, decimal_places=2)
    year = models.IntegerField()
    

    def __str__(self) -> str:
        return f'{self.holiday_list}:{self.year}'
    
    class Meta:
        ordering=('-created_at', )


class Shift(SimplifyBaseModel):
    name = models.CharField(max_length=30)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # duration = models.DecimalField(max_digits=5, decimal_places=2)
    shift_duration = models.TimeField()
    sat = models.BooleanField(default=False)
    sun = models.BooleanField(default=False)
    mon = models.BooleanField(default=False)
    tue = models.BooleanField(default=False)
    wed = models.BooleanField(default=False)
    thu = models.BooleanField(default=False)
    fri = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        ordering=('-created_at', )


class Employee(BaseModel):
    device = models.ForeignKey(TADevice, on_delete=models.PROTECT, related_name='employee_device')
    device_id_no = models.IntegerField()
    emp_id_no = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name='employee_list')
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT, related_name='shift_employee')
    card_no = models.IntegerField()

    def __str__(self):
        return f'{self.emp_id_no}:{self.name}'
    
    class Meta:
        ordering=('-created_at', )
        constraints = [
            UniqueConstraint(fields=['device', 'emp_id_no'], name='unique_device_emp')
        ]


class Attendance(BaseModel):
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='attend_emp')
    punch_in_device = models.ForeignKey(TADevice, on_delete=models.PROTECT, related_name='attendance_in')
    punch_in_date = models.DateField()
    punch_in_time = models.TimeField()
    
    punch_out_device = models.ForeignKey(TADevice, on_delete=models.PROTECT, related_name='attendance_out', blank=True, null=True)
    punch_out_date = models.DateField(blank=True, null=True)
    punch_out_time = models.TimeField(blank=True, null=True)

    duration = models.TimeField(blank=True, null=True)
    # working_hour = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    status = models.BooleanField(default=False)  # in-time/late
    late_count = models.TimeField(blank=True, null=True)  # count in minitue

    class Meta:
        ordering=('-created_at', )
        constraints = [
            UniqueConstraint(fields=['emp', 'punch_in_date'], name='unique_emp_date')
        ]