from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile
from django.forms.models import ModelForm

from django.forms.widgets import FileInput

from django_recaptcha.fields import ReCaptchaField

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        captcha = ReCaptchaField()
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'profile_img': FileInput(),
        }
