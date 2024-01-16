from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group", "image")
        labels = {'text' : 'Ваши мысли',
                  'group' : 'Выбор группу',
                  'image': 'Изображение'}
        help_text = {'text' : 'Напишите пост',
                     'group' : 'Выберете группу',
                     'image': 'Выберете изображение'}
    def clean_text(self):
        data = self.cleaned_data["text"]
        if data.replace(' ', '') == '':
            raise forms.ValidationError(
                'Заполните форму'
            )
        return data
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text' : 'Ваши мысли'}
        help_text = {'text' : 'Напишите комментарий'}
                 
        