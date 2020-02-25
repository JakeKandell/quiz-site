from django.urls import path

from . import views


app_name = 'quiz'
urlpatterns = [
    # ex: /quiz/
    path('', views.index, name='index'),

    # ex: /quiz/5/
    path('<int:quiz_id>/', views.single_quiz, name='single_quiz'),

    # ex: /quiz/5/3/
    path('<int:quiz_id>/<int:question_id>/', views.single_question, name='single_question'),

    # ex: /quiz/5/3/vote/
    path('<int:quiz_id>/<int:question_id>/vote/', views.vote, name='vote'),

    # ex: /quiz/5/results/
    path('<int:quiz_id>/results/', views.results, name='results'),

    # ex: /quiz/create/
    path('create/', views.create_quiz, name='create_quiz'),

    # ex: /quiz/create/7/2/
    path('create/<int:quiz_id>/<int:question_id>/', views.create_question, name='create_question'),

]