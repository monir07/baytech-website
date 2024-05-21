from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from ta_device.models import (Department, Section)

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['device_status'].widget.attrs['class'] ='select2_single form-control'
        
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


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('department_list','name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['device_status'].widget.attrs['class'] ='select2_single form-control'
        self.fields['department_list'].label ='Select Department'
        
        field_list = self.Meta.fields
        self.helper = FormHelper()
        # self.helper.form_method = 'get' # get or post
        self.helper.layout = Layout()
        # form fields layout.
        column_fields = []
        for field in field_list:
            column_fields.append(Column(f'{field}', css_class='form-group col-md-6 mb-0'))
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