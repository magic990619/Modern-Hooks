from django import forms


class InterviewForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    video = forms.FileField(required=False)
    token = forms.CharField(max_length=50)
    question_order = forms.IntegerField()
    question_count = forms.IntegerField()


class UniversalInterviewForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    job_id = forms.IntegerField()
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=255)
    position = forms.CharField(max_length=255, required=False)
    video = forms.FileField(required=False)
    question_order = forms.IntegerField()
    question_count = forms.IntegerField()
