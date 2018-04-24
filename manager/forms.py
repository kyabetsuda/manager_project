from django import forms

class RegisterForm(forms.Form):
    # アカウント名
    identifier = forms.CharField()
    # 名前
    name = forms.CharField()
    #パスワード
    password = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 5:
            raise forms.ValidationError("Not enough char!")
        return name
