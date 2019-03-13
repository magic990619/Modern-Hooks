from django import forms

from vw_client_groups.models import SubClientGroup, ClientGroup


class ClientGroupAdminForm(forms.ModelForm):
    class Meta:
        model = ClientGroup
        fields = '__all__'


class SubClientGroupAdminForm(forms.ModelForm):
    class Meta:
        model = SubClientGroup
        # fields = '__all__'
        exclude = ('client_group',)

    def __init__(self, *args, **kwargs):
        super(SubClientGroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['users'].queryset = SubClientGroup.objects.get(
                id=self.instance.id).client_group.users.all()
