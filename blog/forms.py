from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post


class PostForm(forms.ModelForm):
    required_css_class = 'my-custom-class'
    title = forms.CharField(max_length=40)

    class Meta:
        model = Post
        fields = ['title', 'author', 'post_type', 'category', 'text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control"})
        self.fields['title'].label = "Заголовок публикации"
        self.fields['title'].widget.attrs.update({'placeholder': "Введите название"})
        self.fields['text'].label = "Текст публикации"
        self.fields['text'].widget.attrs.update({'placeholder': "Введите текст"})

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Текст статьи не должен быть идентичен заголовку."
            )
        return cleaned_data


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user