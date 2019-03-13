from django import forms

from .models import SampleQuestion


class SampleQuestionForm(forms.ModelForm):
    type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )

    class Meta:
        model = SampleQuestion
        fields = ('type', 'content', 'limit',)

    def __init__(self, *args, **kwargs):
        super(SampleQuestionForm, self).__init__(*args, **kwargs)
        self.fields['limit'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
        })
