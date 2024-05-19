from django.db import models
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
        return f'{self.start_time}:{self.end_time}'
    
    class Meta:
        ordering = ('-created_at',)


class Department(SimplifyBaseModel):
    name = models.CharField(max_length=80)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        ordering=('-created_at', )


class Section(SimplifyBaseModel):
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='selction_list')
    name = models.CharField(max_length=80)

    def __str__(self) -> str:
        return f'{self.department.name}:{self.name}'
    
    class Meta:
        ordering=('-created_at', )


class Holiday(SimplifyBaseModel):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        ordering=('-created_at', )


class HolidayCalender(SimplifyBaseModel):
    holiday = models.ForeignKey(Holiday, on_delete=models.CASCADE, related_name='holiday_calender')
    date_from = models.DateField()
    date_to = models.DateField()
    total_day = models.DecimalField(max_digits=5)
    year = models.IntegerField()
    

    def __str__(self) -> str:
        return f'{self.holiday}:{self.year}'
    
    class Meta:
        ordering=('-created_at', )


class Shift(SimplifyBaseModel):
    name = models.CharField(max_length=30)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.DecimalField(max_digits=5)
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
    device = models.ForeignKey(TADevice, on_delete=models.CASCADE, related_name='employee_device')
    emp_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='employee_list')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='shift_employee')
    card_no = models.IntegerField()
    device_id = models.IntegerField()

    def __str__(self):
        return f'{self.emp_id}:{self.name}'
    
    class Meta:
        ordering=('-created_at', )


class Attendance(BaseModel):
    emp = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='attend_emp')
    punch_in_date = models.DateField()
    punch_in_time = models.TimeField()
    punch_in_device = models.TimeField()
    
    punch_out_date = models.DateField()
    punch_out_time = models.TimeField()
    punch_out_device = models.TimeField()

    working_hour = models.DecimalField(max_digits=5)
    status = models.BooleanField(default=False)  # in-time/late
    late_count = models.DecimalField(max_digits=5, blank=True, null=True)  # count in minitue