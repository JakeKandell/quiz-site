from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CreateQuizForm(forms.Form):
    quiz_name = forms.CharField(max_length=50, label="Quiz Name")
    num_questions = forms.IntegerField(label="Number of Questions")

    def clean_name(self):
        data = self.cleaned_data['quiz_name']

        # # Check if a date is not in the past.
        if data == "Default_Name":
            raise ValidationError(_('Invalid name - Must be Unique'))

        # Remember to always return the cleaned data.
        return data

    def clean_num_questions(self):
        data = self.cleaned_data['num_questions']

        # # Check if a date is not in the past.
        if (isinstance(data, int) == False) or (data < 1):
            raise ValidationError(_('Invalid number - must be positive integer)') )

        # Remember to always return the cleaned data.
        return data


def 