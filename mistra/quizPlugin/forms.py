from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Question, Answer


class QuestionAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Question
        fields = '__all__'


class AnswerAdminForm(forms.ModelForm):
    correction = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Answer
        fields = '__all__'
