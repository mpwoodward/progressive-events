from django import forms

from .models import User


class AccountCreationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(AccountCreationForm, self).clean()

        if not cleaned_data.get('password') == cleaned_data.get('confirm_password'):
            self.add_error('password', "The passwords don't match.")
            self.add_error('confirm_password', "The passwords don't match.")

        try:
            User.objects.get(email=cleaned_data.get('email'))
            self.add_error('email', 'An account with that email address already exists.')
        except User.DoesNotExist:
            pass  # no dupe email so can safely ignore

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'zip', 'password', 'confirm_password']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
        }
