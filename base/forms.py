from django import forms
from django.contrib import messages
from base.models import BaseModel

class SearchFrom(forms.Form):
    search = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Search Anything'}))


class FilterFrom(SearchFrom):
    from_date = forms.DateField(label='', required=False, widget=forms.DateInput(
        format='%d-%m-%Y', attrs={'type': 'date'}))

    to_date = forms.DateField(label='', required=False, widget=forms.DateInput(
        format='%d-%m-%Y', attrs={'type': 'date'}))


class DateFilterForm(forms.Form):
    date = forms.DateField(label='', required=False, widget=forms.DateInput(
        format='%d-%m-%Y', attrs={'type': 'date'}))


class BaseModelForm(forms.ModelForm):
    # activation_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}))
    class Meta:
        model = BaseModel
        exclude = ['created_at', 'updated_at', 'created_by', 'updated_by']

    # def is_valid(self) -> bool:
    #     request = self.kwargs.get("request")
    #     if request.user != self.instance.user:
    #         messages.error(request, "You are not the creator of this object!")
    #         return False
    #     return super().is_valid()

    # def __init__(self, *args, **kwargs):
    #     super(BaseModelForm, self).__init__(*args, **kwargs)
    #     for field in self.Meta.fields:
    #         self.fields[field].required = True
    #         self.fields[field].label = str(self.fields[field].label).title()
    #     self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.filter(Q(userinform__is_retired=False, userinform__is_terminate=False)))
    #     self.fields['user'].widget.attrs['class'] = 'select2-show-search'
    #     self.fields['user'].label = 'Select User'
