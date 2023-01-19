from django.forms import ModelForm

from posts.models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        labels = {'group': 'Группа', 'text': 'Текст поста'}
        help_texts = {'group': 'Выберите группу',
                      'text': 'Введите текст поста'}
        fields = ('group', 'text', 'image')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
