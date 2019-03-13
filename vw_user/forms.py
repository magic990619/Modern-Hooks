from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import UsernameField
from django.utils.translation import ugettext_lazy as _


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = ''
        self.fields['login'].widget = forms.TextInput(attrs={
            'placeholder': 'Username',
            'autofocus': 'autofocus',
            'class': 'form-control top',
        })
        self.fields['password'].label = ''
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control bottom',
        })


class AdminCreateUserForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", 'is_staff', 'client_group',)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(AdminCreateUserForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'),
                                              self.instance)
        return password2

    def save(self, commit=True):
        user = super(AdminCreateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
