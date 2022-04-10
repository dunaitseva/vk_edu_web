from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.paginator import Paginator


def get_tags():
    tags = [
        'C++',
        'Python',
        'SQL',
        'Django',
        'Ruby',
        'Boost'
    ]
    return tags


def questions_plug_loader(*args, **kwargs):
    common_question_data = {
        'question': {
            'id': 4,
            'title': 'Common title',
            'text': 'Common question text',
            'time': None,
            'author': 'Nickname',
        },
        'tags': get_tags(),
        'answers_counter': 12,
        'likes_counter': 23,
        'author_avatar': None
    }
    result_questions_query = [common_question_data for i in range(32)]
    return result_questions_query


class DefaultQuestionContainPageView(View):
    QUESTIONS_PER_PAGE = 5
    template = 'base.html'
    question_objects_template_naming = 'questions'
    questions_loader = questions_plug_loader
    loader_specific_args = []
    loader_specific_kwargs = dict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paginator = None

    def resolve_pagination(self, page: int):
        rendering_page_objects = self.paginator.get_page(page)
        return rendering_page_objects

    def get_view_specific_data(self, request, *args, **kwargs):
        return {'tags': get_tags()}

    def prepare_questions_query(self):
        questions_objects = questions_plug_loader(
            *self.loader_specific_args,
            **self.loader_specific_kwargs
        )
        self.paginator = Paginator(questions_objects, self.QUESTIONS_PER_PAGE)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.prepare_questions_query()
        passing_arguments = self.get_view_specific_data(request, *args, **kwargs)
        page_number = int(request.GET.get('page', 1))
        question_objects = self.resolve_pagination(page_number)
        passing_arguments.update({self.question_objects_template_naming: question_objects})
        return render(
            request,
            self.template,
            passing_arguments
        )


class IndexView(DefaultQuestionContainPageView):
    template = 'index.html'


class HotQuestionsView(DefaultQuestionContainPageView):
    template = 'hot.html'


class TagQuestionsView(DefaultQuestionContainPageView):
    template = 'tag.html'

    def get_view_specific_data(self, request, *args, **kwargs):
        return {'tag_name': kwargs.get('tag_name'), 'tags': get_tags()}


def concrete_questions_plug_loader(question):
    common_answer_data = {
        'answer': {
            'id': question['question']['id'],
            'text': 'Common answer text',
            'correct': True,
            'time': None,
            'author': 'Nickname',
            'question': question
        },
        'author_avatar': None
    }

    return [common_answer_data for _ in range(12)]


def question_get_plug(q_id):
    common_question_data = {
        'question': {
            'id': 4,
            'title': 'Common title',
            'text': 'Common question text',
            'time': None,
            'author': 'Nickname',
        },
        'tags': get_tags(),
        'answers_counter': 12,
        'likes_counter': 23,
        'author_avatar': None
    }
    return common_question_data


class ConcreteQuestionView(View):
    ANSWERS_PER_PAGE = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paginator = None

    def resolve_pagination(self, page: int):
        rendering_page = self.paginator.get_page(page)
        return rendering_page

    def prepare_questions_query(self, question):
        answer_objects = concrete_questions_plug_loader(question)
        self.paginator = Paginator(answer_objects, self.ANSWERS_PER_PAGE)

    def prepare_arguments(self, request, *args, **kwargs):
        return {'tags': get_tags()}

    def get(self, request: HttpRequest, question_id) -> HttpResponse:
        question = question_get_plug(question_id)
        self.prepare_questions_query(question)
        page_number = int(request.GET.get('page', 1))
        passing_arguments = self.prepare_arguments(request)
        passing_arguments.update({'question': question})
        passing_arguments.update({'answers': self.resolve_pagination(page_number)})
        return render(request, "question.html", passing_arguments)


class LoginView(View):
    def prepare_arguments(self, request, *args, **kwargs):
        return dict()

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'login.html', self.prepare_arguments(request))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return redirect('/')


class RegisterView(View):
    def prepare_arguments(self, request, *args, **kwargs):
        return dict()

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'register.html', self.prepare_arguments(request))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return redirect('/')


class AskView(View):
    def prepare_arguments(self, request, *args, **kwargs):
        return {'tags': get_tags()}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'ask.html', self.prepare_arguments(request))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return redirect('/')


class SettingsView(View):
    def prepare_arguments(self, request, *args, **kwargs):
        return dict()

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'settings.html', self.prepare_arguments(request))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return redirect('/')
