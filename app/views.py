from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.paginator import Paginator


class DefaultQuestionContainPageView(View):
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
        rendering_page_objects = self.paginator.get_page(page)
        return rendering_page_objects

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tags': self.tags}

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        page_number = int(request.GET.get('page', 1))
        question_objects = self.resolve_pagination(page_number)
        passing_arguments = self.prepare_arguments(request, *args, **kwargs)
        passing_arguments.update({self.iterable_objects: question_objects})
        return render(
            request,
            self.template,
            passing_arguments
        )


class IndexView(DefaultQuestionContainPageView):
    tmp_questions_amount = 23
    QUESTIONS_PER_PAGE = 5
    template = 'index.html'
    iterable_objects = 'questions'


class HotQuestionsView(DefaultQuestionContainPageView):
    tmp_questions_amount = 12
    QUESTIONS_PER_PAGE = 5
    template = 'hot.html'
    iterable_objects = 'questions'


class TagQuestionsView(DefaultQuestionContainPageView):
    tmp_questions_amount = 12
    QUESTIONS_PER_PAGE = 5
    template = 'tag.html'
    iterable_objects = 'questions'

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tag_name': kwargs.get('tag_name'), 'tags': self.tags}


class ConcreteQuestionView(View):
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
