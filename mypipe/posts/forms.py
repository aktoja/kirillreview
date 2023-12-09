from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group")
        labels = {'text' : 'Ваши мысли',
                  'group' : 'Выбор группу'}
        help_text = {'text' : 'Напишите пост',
                     'group' : 'Выберете группу'}
    def clean_text(self):
        data = self.cleaned_data["text"]
        if data.replace(' ', '') == '':
            raise forms.ValidationError(
                'Заполните форму'
            )
        return data