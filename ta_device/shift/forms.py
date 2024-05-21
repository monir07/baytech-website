from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from ta_device.models import (Shift)

class ShiftForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    class Meta:
        model = Shift
        fields = ('name', 'start_time', 'end_time', 'sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['device_status'].widget.attrs['class'] ='select2_single form-control'
        
        
        self.helper = FormHelper()
        # self.helper.form_method = 'get' # get or post
        self.helper.layout = Layout()
        # form fields layout.
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('start_time', css_class='form-group col-md-4 mb-0'),
                Column('end_time',css_class='form-group col-md-4 mb-0'),
                css_class='row'
            ),
            Row(
                Column('sat', css_class='form-group col-md-1 mb-0'),
                Column('sun',css_class='form-group col-md-1 mb-0'),
                Column('mon',css_class='form-group col-md-1 mb-0'),
                Column('tue',css_class='form-group col-md-1 mb-0'),
                Column('wed',css_class='form-group col-md-1 mb-0'),
                Column('thu',css_class='form-group col-md-1 mb-0'),
                Column('fri',css_class='form-group col-md-1 mb-0'),
                css_class='row'
            ),
            Row(
                Column(Button('cancel', 'Go Back', css_class='btn-secondary btn-block', onclick="history.back()"), css_class='form-group col-md-3'),
                Column(Submit('submit', 'Update' if self.instance.pk else 'Submit', css_class='btn-primary btn-block'), css_class='form-group col-md-3'),
                css_class='row'
            ),
        )
        