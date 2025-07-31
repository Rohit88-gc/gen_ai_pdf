from django import forms
from .models import UploadedPDF

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedPDF
        fields = ['title', 'pdf_file']

class QuestionForm(forms.Form):
    question = forms.CharField(label='Ask something:', max_length=200)