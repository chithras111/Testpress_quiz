from django import forms
from schoolquiz.models import quiz
class quizform(forms.ModelForm):
    class Meta:
        model=quiz
        fields='__all__'