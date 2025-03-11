from django import forms
from page.models import ContactUs
from captcha.fields import CaptchaField


class ContactUsForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = ContactUs
        fields = ('name', 'email_address', 'subject', 'message', 'contact_no')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Your name here'}),
            'email_address': forms.DateInput(attrs={'class': 'form-control', 'placeholder':'Your email here'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your subject here'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Tell us a few words', 'rows':'3'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your phone here'}),
        }


class DockingCertificateSearchForm(forms.Form):
    certificate_no = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder':'Insert Docking Certificate No'}),)
