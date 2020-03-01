from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Quiz, Question, Choice

from .forms import CreateQuizForm, CreateQuestionForm


# Create your views here.

# index page of all quizzes
def index(request):
    all_quiz_list = Quiz.objects.all()
    context = {
        'all_quiz_list': all_quiz_list,
    }

    return render(request, 'quiz/index.html', context)


# specific quiz splash screen
def single_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    num_questions = len(quiz.question_set.all())

    # deletes quiz and returns to home if no questions created
    if num_questions == 0:
        quiz.delete()
        all_quiz_list = Quiz.objects.all()
        context = {
            'all_quiz_list': all_quiz_list,
        }
        return render(request, 'quiz/index.html', context)

    quiz.num_questions = num_questions
    quiz.save()

    # resets accuracy info to 0
    request.session["num_correct"] = 0
    request.session["num_wrong"] = 0

    context = {
        'quiz': quiz,
        'num_questions': num_questions,
    }

    return render(request, 'quiz/single_quiz.html', context)


# specific question view
def single_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    current_question = quiz.question_set.get(question_num=question_id)

    # Checks if currently on last question of quiz
    next_or_submit = "Next"
    last_question_check = False
    if question_id == (len(quiz.question_set.all())):
        last_question_check = True
        next_or_submit = "Submit"

    next_question_id = question_id+1

    all_choices = current_question.choice_set.all()

    context = {
        'current_question': current_question,
        'all_choices': all_choices,
        'quiz': quiz,
        'next_question_id': next_question_id,
        'last_question_check': last_question_check,
        'next_or_submit': next_or_submit
    }

    return render(request, 'quiz/single_question.html', context)


# view that receives info from user's answer to question and determines correctness
def vote(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    current_question = quiz.question_set.get(question_num=question_id)

    # checks if current question is last one
    next_or_submit = "Next"
    if question_id == (len(quiz.question_set.all())):
        next_or_submit = "Submit"

    try:
        selected_choice = current_question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'quiz/single_question.html', {
            'quiz': quiz,
            'current_question': current_question,
            'error_message': "You didn't select a choice.",
            'next_or_submit': next_or_submit,
        })
    else:

        # get which choice is the correct answer
        correct_answer = current_question.choice_set.get(correct=True)

        if selected_choice == correct_answer:
            print("You are right")
            request.session["num_correct"] += 1
        else:
            print("You are wrong")
            request.session["num_wrong"] += 1

        # checks if next page should be results or next question
        if question_id == (len(quiz.question_set.all())):
            return HttpResponseRedirect(reverse('quiz:results', args=(quiz.id,)))
        else :
            return HttpResponseRedirect(reverse('quiz:single_question', args=(quiz.id, question_id+1,)))


# quiz results page
def results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    num_correct = request.session["num_correct"]
    num_wrong = request.session["num_wrong"]

    total_questions = num_correct+num_wrong

    # formats accuracy as % with no decimal digits
    accuracy = num_correct/(total_questions)

    accuracy_over_75 = False
    if accuracy >= .75:
        accuracy_over_75 = True

    accuracy_formatted = "{:.0%}".format(accuracy)

    context = {
        'num_correct': num_correct,
        'num_wrong': num_wrong,
        'accuracy_over_75': accuracy_over_75,
        'accuracy_formatted': accuracy_formatted,
        'total_questions': total_questions,
        'quiz': quiz,
    }
    return render(request, 'quiz/results.html', context)


# view for create quiz page
def create_quiz(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreateQuizForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            quiz_name = form.cleaned_data['quiz_name']
            num_questions = form.cleaned_data['num_questions']

            new_quiz = Quiz(quiz_title=quiz_name, num_questions=num_questions)
            new_quiz.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('quiz:create_question', args=(new_quiz.id, 1,)))

    # If this is a GET (or any other method) create the default form.
    else:
        form = CreateQuizForm()

    context = {
        'form': form,
    }

    return render(request, 'quiz/create_quiz.html', context)


# view for create quiz page
def create_question(request, quiz_id, question_id):

    # gets current quiz
    quiz = Quiz.objects.get(pk=quiz_id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreateQuestionForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            question_text = form.cleaned_data['question_text']

            choice1 = form.cleaned_data["choice1_text"]
            choice1_correctness = form.cleaned_data["choice1_correctness"]

            choice2 = form.cleaned_data["choice2_text"]
            choice2_correctness = form.cleaned_data["choice2_correctness"]

            choice3 = form.cleaned_data["choice3_text"]
            choice3_correctness = form.cleaned_data["choice3_correctness"]

            choice4 = form.cleaned_data["choice4_text"]
            choice4_correctness = form.cleaned_data["choice4_correctness"]

            # creates question in quiz
            question = Question(quiz=quiz, question_text=question_text, question_num=question_id)
            question.save()

            # creates choices for questions
            question.choice_set.create(choice_text=choice1, correct=choice1_correctness)
            question.choice_set.create(choice_text=choice2, correct=choice2_correctness)
            question.choice_set.create(choice_text=choice3, correct=choice3_correctness)
            question.choice_set.create(choice_text=choice4, correct=choice4_correctness)

            # redirect to home if done or next create question page if not
            if question_id == quiz.num_questions:
                return HttpResponseRedirect(reverse('quiz:index'))
            else:
                return HttpResponseRedirect(reverse('quiz:create_question', args=(quiz_id, question_id+1,)))

    # If this is a GET (or any other method) create the default form.
    else:
        form = CreateQuestionForm()

    if question_id == quiz.num_questions:
        next_submit = "Submit"
    else :
        next_submit = "Next"

    context = {
        'form': form,
        'question_num': question_id,
        'next_submit': next_submit,

    }

    return render(request, 'quiz/create_question.html', context)