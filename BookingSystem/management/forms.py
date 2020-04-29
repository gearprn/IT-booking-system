from django import forms

class adminSignInForm(forms.Form):
    username = forms.CharField(min_length=3, label='ชื่อผู้ใช้ :')
    password = forms.CharField(min_length=8, label='รหัสผ่าน :', widget=forms.PasswordInput)

    username.widget.attrs.update({'class':'form-control'})
    password.widget.attrs.update({'class':'form-control'})



