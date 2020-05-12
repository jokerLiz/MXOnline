from django import forms
from apps.operations.models import UserAsk


class AddAskForm(forms.ModelForm):

    mobile = forms.CharField(max_length=11,min_length=11,required=True)

    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']