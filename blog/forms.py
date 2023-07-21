from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25,
                           label='',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Ваше имя'}))
    email = forms.EmailField(label='',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш E-Mail'}))
    to = forms.EmailField(label='',
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-Mail адрессата'}))
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сообщение'}),
                               label='')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'name', 'email']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст коментария...'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Ваше имя'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Ваш E-Mail'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''


class SearchForm(forms.Form):
    query = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск'}),
                            )
