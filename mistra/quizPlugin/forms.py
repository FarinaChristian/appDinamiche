from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Question, Answer


class QuestionAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = Question
        fields = '__all__'


class AnswerAdminForm(forms.ModelForm):
    correction = forms.CharField(widget=CKEditor5Widget(), required=False)

    class Meta:
        model = Answer
        fields = '__all__'
