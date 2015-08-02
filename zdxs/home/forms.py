from django import forms
from django.contrib.auth.models import User
import re

class LoginForm(forms.Form):
	email=forms.EmailField(label="your email",
				required=True,
				error_messages={'required':'please code your valid email'},
				widget=forms.EmailInput(attrs={"class":'form-control',"placeholder":"write your email here"}))
	password=forms.CharField(label="password",
					required=True,
					error_messages={'required':'password is needed'},
					widget=forms.PasswordInput(attrs={"class":'form-control',"placeholder":"write your password here"})
				)
		

class RegisterForm(forms.Form):
	name=forms.CharField(label="your name",
				max_length=100,
				required=True,
				error_messages={'required':'name is needed!'},
				widget=forms.TextInput(attrs={'class':"form-control","placeholder":"write your unique name"}))
	email=forms.EmailField(label="your email",
				required=True,
				error_messages={'required':'please code your valid email'},
				widget=forms.EmailInput(attrs={"class":'form-control',"placeholder":"write your email here"}))
	password1=forms.CharField(label="password",
					required=True,
					error_messages={'required':'password is needed'},
					widget=forms.PasswordInput(attrs={"class":'form-control',"placeholder":"write your password here"})
				)
	password2=forms.CharField(label="password",
					required=True,
					error_messages={'required':'password is needed'},
					widget=forms.PasswordInput(attrs={"class":'form-control',"placeholder":"to check your password"})
				)

	def clean_name(self):
		name=self.cleaned_data['name']
		if ' ' in name:
			raise forms.ValidationError('no space')
		if not re.search(r'^\w+$',name):
			raise forms.ValidationError('it can only be letters or numbers')
		return name

	def clean_password1(self):
		password=self.cleaned_data['password1']
		cha_num=len(password)
		if cha_num<6:
			raise forms.ValidationError("character must more than 6")
		return password

	def clean_email(self):
		email=self.cleaned_data['email']
		try:
			user=User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('email is already existed!')

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1=self.cleaned_data['password1']
			password2=self.cleaned_data['password2']
			if password1==password2:
				return password2
			raise forms.ValidationError('password1 must equal to password2')
		
