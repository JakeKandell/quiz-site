from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# form to create a new quiz
class CreateQuizForm(forms.Form):
    quiz_name = forms.CharField(max_length=50, label="Quiz Name")
    num_questions = forms.IntegerField(label="Number of Questions")

    def clean_name(self):
        data = self.cleaned_data['quiz_name']

        # Check if quiz name is unique.
        if data == "Default_Name":
            raise ValidationError(_('Invalid name - Must be Unique'))

        # returns cleaned data
        return data

    def clean_num_questions(self):
        data = self.cleaned_data['num_questions']

        # Check if number of questions is at least 1 and is an integer
        if (isinstance(data, int) == False) or (data < 1):
            raise ValidationError(_('Invalid number - must be positive integer'))

        # Remember to always return the cleaned data.
        return data


# form to create questions with choices for each quiz
class CreateQuestionForm(forms.Form):
    question_text = forms.CharField(max_length=300, label="Question Text")

    choice1_text = forms.CharField(max_length=300, label="Choice 1")
    choice1_correctness = forms.BooleanField(label="Choice 1 Correct?", required=False)

    choice2_text = forms.CharField(max_length=300, label="Choice 2")
    choice2_correctness = forms.BooleanField(label="Choice 2 Correct?", required=False)

    choice3_text = forms.CharField(max_length=300, label="Choice 3")
    choice3_correctness = forms.BooleanField(label="Choice 3 Correct?", required=False)

    choice4_text = forms.CharField(max_length=300, label="Choice 4")
    choice4_correctness = forms.BooleanField(label="Choice 4 Correct?", required=False)

    # makes sure that exactly one answer is selected to be true
    def clean(self):

        choice1_answer = self.cleaned_data["choice1_correctness"]
        choice2_answer = self.cleaned_data["choice2_correctness"]
        choice3_answer = self.cleaned_data["choice3_correctness"]
        choice4_answer = self.cleaned_data["choice4_correctness"]

        answer_list = [choice1_answer, choice2_answer, choice3_answer, choice4_answer]

        print(answer_list)

        trueCount = 0
        for answer in answer_list:
            if answer == True:
                trueCount += 1

        if trueCount != 1:
            raise ValidationError(_('Must have exactly one correct answer'))

        return self.cleaned_data