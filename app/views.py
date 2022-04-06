from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.paginator import Paginator


class DefaultQuestionPageView(View):
    # In case of current project we have a lot of pages where
    # logic of viewing is the similar. So I think it's a good idea
    # to use interface of QuestionPageView in other view classes
    # with the same logic. As I understand, models is very flexible
    # instrument, and in final version of this class hierarchy
    # I want only change the model and some specific logic
    # of view to change behaviour.
    tmp_questions_amount = 23
    QUESTIONS_PER_PAGE = 5
    template = 'base.html'
    iterable_objects = 'cards'
    tags = ['C++', 'Python', 'SQL', 'Django', 'Ruby', 'Boost']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions_objects = range(self.tmp_questions_amount)
        self.paginator = Paginator(self.questions_objects, self.QUESTIONS_PER_PAGE)

    def resolve_pagination(self, page: int):
        rendering_page = self.paginator.get_page(page)
        return rendering_page

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tags': self.tags}

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        page = int(request.GET.get('page', 1))
        question_objects = self.resolve_pagination(page)
        passing_arguments = self.prepare_arguments(request, *args, **kwargs)
        passing_arguments.update({self.iterable_objects: question_objects})
        return render(
            request,
            self.template,
            passing_arguments
        )


class IndexView(DefaultQuestionPageView):
    tmp_questions_amount = 23
    QUESTIONS_PER_PAGE = 5
    template = 'index.html'
    iterable_objects = 'questions'


class HotQuestionsView(DefaultQuestionPageView):
    tmp_questions_amount = 12
    QUESTIONS_PER_PAGE = 5
    template = 'hot.html'
    iterable_objects = 'questions'


class TagQuestionsView(DefaultQuestionPageView):
    tmp_questions_amount = 12
    QUESTIONS_PER_PAGE = 5
    template = 'tag.html'
    iterable_objects = 'questions'

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tag_name': kwargs.get('tag_name'), 'tags': self.tags}


class QuestionView(View):
    tmp_answers_amount = 8
    ANSWERS_PER_PAGE = 5
    tags = ['C++', 'Python', 'SQL', 'Django', 'Ruby', 'Boost']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer_objects = range(self.tmp_answers_amount)
        self.paginator = Paginator(self.answer_objects, self.ANSWERS_PER_PAGE)

    def resolve_pagination(self, page: int):
        rendering_page = self.paginator.get_page(page)
        return rendering_page

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tags': self.tags}

    def get(self, request: HttpRequest, question_id) -> HttpResponse:
        page = int(request.GET.get('page', 1))
        passing_arguments = self.prepare_arguments(request)
        passing_arguments.update({'q_id': question_id})
        passing_arguments.update({'answers': self.resolve_pagination(page)})
        return render(request, "question.html", passing_arguments)


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
