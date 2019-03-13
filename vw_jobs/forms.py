from django import forms

from vw_jobs.models import Jobs
from vw_user.models import CustomizedUser


class JobCreateForm(forms.ModelForm):
    link = forms.CharField(required=False)
    user = forms.ModelChoiceField(required=False, queryset=CustomizedUser.objects.all())

    class Meta:
        model = Jobs
        fields = ('user', 'link', 'position',)
