from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name','password1','password2', 'phone_number', 'profile_pic']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', None)
        try:
            int(phone)
        except (ValueError, TypeError):
            raise forms.ValidationError('Please enter a valid phone number')
        return phone


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ['email', 'password', 'is_active']

    def clean_password(self):
        return self.initial["password"]
        

class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','password']