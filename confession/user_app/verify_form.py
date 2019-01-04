from django import forms

from user_app.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'u_name',
            'icon',
            'sex',
            'age',
        ]

    def clean_age(self):
        clean_data = super().clean()
        if (clean_data['age'] < 10) and (clean_data['age'] > 50):
            raise forms.ValidationError('输入的年龄不切合实际')
        return clean_data['age']