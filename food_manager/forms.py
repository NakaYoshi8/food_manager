from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from .models import User, Category, Tag, Food


class SignUpForm(UserCreationForm):
    '''会員登録用'''

    class Meta:
        model = User
        fields = ('username', 'email')

# アカウント設定画面用
class UsernameForm(forms.ModelForm):
    '''ユーザ名変更用'''
    
    class Meta:
        model = User
        fields = ('username',)
        labels = {'username': '',}
        help_texts = {'username': None,}  # 「この項目は必須です...」を非表示


class EmailForm(forms.ModelForm):
    '''メールアドレス変更用'''

    class Meta:
        model = User
        fields = ('email',)
        labels = {'email': '',}


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更用"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CategoryForm(forms.ModelForm):
    '''カテゴリ追加・編集用'''

    class Meta:
        model = Category
        fields = ('category_name',)
        labels = {'category_name': 'カテゴリ名',}


class TagForm(forms.ModelForm):
    '''タグ追加・編集用'''

    class Meta:
        model = Tag
        fields = ('tag_name', 'category',)
        labels = {
            'tag_name': 'タグ名',
            'category': 'カテゴリ名',
        }


class FoodForm(forms.ModelForm):
    '''食品追加用'''

    class Meta:
        model = Food
        fields = ('food_name', 'date', 'quantity', 'unit', 'description',)
        widgets = {
            'date': forms.SelectDateWidget
        }
        labels = {
            'food_name': '食品名',
            'date': '賞味期限',
            'quantity': '数量',
            'unit': '単位',
            'description': '説明',
        }

# 食品詳細ページ用
class FoodNameForm(forms.ModelForm):
    '''食品名編集用'''

    class Meta:
        model = Food
        fields = ('food_name',)
        labels = {'food_name': ''}


class FoodDateForm(forms.ModelForm):
    '''食品の賞味期限編集用'''

    class Meta:
        model = Food
        fields = ('date',)
        widgets = {
            'date': forms.SelectDateWidget
        }
        labels = {'date': ''}


class FoodQuantityForm(forms.ModelForm):
    '''食品の数量編集用'''
    
    class Meta:
        model = Food
        fields = ('quantity',)
        labels = {'quantity': ''}


class FoodUnitForm(forms.ModelForm):
    '''食品の数量単位編集用'''

    class Meta:
        model = Food
        fields = ('unit',)
        labels = {'unit': ''}


class FoodDescriptionForm(forms.ModelForm):
    '''食品の説明テキスト編集用'''

    class Meta:
        model = Food
        fields = ('description',)
        labels = {'description': ''}