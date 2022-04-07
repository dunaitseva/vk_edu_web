from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.paginator import Paginator
from .models import Question, Tag, Like, Answer, Profile
from questions.settings import MEDIA_ROOT


class DefaultQuestionPageView(View):
    # In case of current project we have a lot of pages where
    # logic of viewing is the similar. So I think it's a good idea
    # to use interface of QuestionPageView in other view classes
    # with the same logic. As I understand, models is very flexible
    # instrument, and in final version of this class hierarchy
    # I want only change the model and some specific logic
    # of view to change behaviour.
    specific_questions_call = Question.objects.all
    specific_questions_call_args = []
    specific_questions_call_kwargs = dict()
    QUESTIONS_PER_PAGE = 5
    template = 'base.html'
    iterable_objects = 'questions'

    def wrap_question_obj(self, question_objects):
        result_query = []
        for question in question_objects:
            item = {
                'question': question,
                'tags': Tag.objects.question_tags(question.id),
                'likes_counter': Like.objects.count_question_likes(question.id),
                'answers_counter': Answer.objects.count_question_answers(question.id),
                'author_avatar': f'/{MEDIA_ROOT}{Profile.objects.get_avatar(question.author.id)}'
            }
            result_query.append(item)
        return result_query

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paginator = None
        self.questions_objects = None

    def resolve_pagination(self, page: int):
        rendering_page = self.paginator.get_page(page)
        return rendering_page

    def prepare_data(self, request, *args, **kwargs):
        self.questions_objects = self.specific_questions_call(
            *self.specific_questions_call_args,
            **self.specific_questions_call_kwargs
        )

        self.paginator = Paginator(
            self.wrap_question_obj(self.questions_objects),
            self.QUESTIONS_PER_PAGE
        )

        return dict()

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        passing_arguments = self.prepare_data(request, *args, **kwargs)
        page = int(request.GET.get('page', 1))
        question_objects = self.resolve_pagination(page)
        passing_arguments.update({self.iterable_objects: question_objects})
        return render(
            request,
            self.template,
            passing_arguments
        )


class IndexView(DefaultQuestionPageView):
    specific_questions_call = Question.objects.all
    template = 'index.html'


class HotQuestionsView(DefaultQuestionPageView):
    specific_questions_call = Question.objects.get_hot
    QUESTIONS_PER_PAGE = 5
    LIKES_TO_HOT = 1
    specific_questions_call_kwargs = dict(likes_to_hot=LIKES_TO_HOT)
    template = 'hot.html'


class TagQuestionsView(DefaultQuestionPageView):
    specific_questions_call = Question.objects.get_tagged_question
    specific_questions_call_kwargs = dict()
    QUESTIONS_PER_PAGE = 5
    template = 'tag.html'
    iterable_objects = 'questions'

    def prepare_data(self, request, *args, **kwargs):
        self.specific_questions_call_kwargs = {'tag_name': kwargs.get('tag_name')}
        result = super().prepare_data(request, *args, **kwargs)
        result.update({'tag_name': kwargs.get('tag_name')})
        return result


class QuestionView(View):
    tmp_answers_amount = 8
    ANSWERS_PER_PAGE = 5
    tags = ['C++', 'Python', 'SQL', 'Django', 'Ruby', 'Boost']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer_objects = range(self.tmp_answers_amount)
        self.paginator = None

    def resolve_pagination(self, page: int):
        rendering_page = self.paginator.get_page(page)
        return rendering_page

    def prepare_paginator(self, question_id):
        answers_objects = Answer.objects.question_answers(question_id)
        self.paginator = Paginator(answers_objects, self.ANSWERS_PER_PAGE)

    def prepare_arguments(self, request, question_id, page):
        self.prepare_paginator(question_id)
        result_query = {
            'answers': self.resolve_pagination(page),
            'question': Question.objects.filter(pk=question_id)[0],
            'tags': Tag.objects.question_tags(question_id)
        }
        return result_query

    def get(self, request: HttpRequest, question_id) -> HttpResponse:
        page = int(request.GET.get('page', 1))
        return render(request, "question.html", self.prepare_arguments(request, question_id, page))


class LoginView(View):
    tags = ['C++', 'Python', 'SQL', 'Django', 'Ruby', 'Boost']

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tags': self.tags}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'login.html', self.prepare_arguments(request))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return redirect('/')


class RegisterView(View):
    tags = ['C++', 'Python', 'SQL', 'Django', 'Ruby', 'Boost']

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tags': self.tags}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'register.html', self.prepare_arguments(request))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return redirect('/')


class AskView(View):
    tags = ['C++', 'Python', 'SQL', 'Django', 'Ruby', 'Boost']

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tags': self.tags}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'ask.html', self.prepare_arguments(request))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return redirect('/')


class SettingsView(View):
    tags = ['C++', 'Python', 'SQL', 'Django', 'Ruby', 'Boost']

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tags': self.tags}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'settings.html', self.prepare_arguments(request))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return redirect('/')
