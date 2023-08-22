from django import forms
from captcha.fields import CaptchaField,CaptchaTextInput
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs={"class":'form-control','placeholder':'请填写用户名','autofocus':''}))
    password = forms.CharField(label="密码",max_length=128,widget=forms.PasswordInput(attrs={"class":'form-control','placeholder':'请填写密码'}))
    captcha = CaptchaField(label="验证码", widget= CaptchaTextInput(attrs={"class":"form-control","placeholder":"captcha"}))



