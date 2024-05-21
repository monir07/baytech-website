from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from ta_device.models import (TADevice)

class TADeviceForm(forms.ModelForm):
    class Meta:
        model = TADevice
        fields = ('device_name', 'ip_address', 'device_status')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['device_status'].widget.attrs['class'] ='select2_single form-control'
        self.fields['device_status'].help_text ='I am declaring this device will be active.'
        
        field_list = self.Meta.fields
        self.helper = FormHelper()
        # self.helper.form_method = 'get' # get or post
        self.helper.layout = Layout()
        # form fields layout.
        column_fields = []
        for field in field_list:
            column_fields.append(Column(f'{field}', css_class='form-group col-md-4 mb-0'))
        self.helper.layout.append(Row(
            *column_fields,
            css_class='row',
        ))
        # submit section btn
        self.helper.layout.append(Row(
            Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
            Column(Submit('submit', 'Update' if self.instance.pk else 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
            css_class='row'
        ))