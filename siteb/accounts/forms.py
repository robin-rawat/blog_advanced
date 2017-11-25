from django import forms
from django.contrib.auth import (authenticate, get_user_model,login,logout)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exists")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")
			return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
			'password2',
		]
	def clean_password2(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if (password != password2):
			raise forms.ValidationError("Password does not match")
		return password
	def clean_username(self):
		username = self.cleaned_data.get("username")
		username_qs = User.objects.filter(username=username)
		if username_qs.exists():
			raise forms.ValidationError("username already exists")
		return username