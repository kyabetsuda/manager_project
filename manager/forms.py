from django import forms

class RegisterForm(forms.Form):
    # アカウント名
    identifier = forms.CharField()
    # 名前
    name = forms.CharField()
    #パスワード
    password = forms.CharField()
    # メールアドレス
    email = forms.EmailField()
    # 誕生日
    birth_year = forms.IntegerField()
    birth_month = forms.IntegerField()
    birth_day = forms.IntegerField()
    # 性別
    sex = forms.IntegerField()
    # 出身地
    address_from = forms.IntegerField()
    # 現住所
    current_address = forms.IntegerField()

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 5:
            raise forms.ValidationError("Not enough char!")
        return name
