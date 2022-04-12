from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.paginator import Paginator

from app.models import Question, Tag, Like, Answer, Profile


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


def load_question_data(question):
    question_item = {
        'question': question,
        'tags': Tag.objects.question_tags(question.id),
        'likes_counter': Like.objects.count_question_likes(question.id),
        'answers_counter': Answer.objects.count_question_answers(question.id),
        'author_avatar': Profile.objects.get_avatar_url(question.author.id)
    }
    return question_item


class DefaultQuestionsContainPageView(View):
    QUESTIONS_PER_PAGE = 5
    template = 'base.html'
    question_objects_template_naming = 'questions'
    questions_loader = Question.objects.all
    loader_specific_args = []
    loader_specific_kwargs = dict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paginator = None

    def load_questions(self, *args, **kwargs):
        loaded_questions = self.questions_loader(*args, **kwargs)
        result_questions_query = []
        for question in loaded_questions:
            question_item = load_question_data(question)
            result_questions_query.append(question_item)
        return result_questions_query

    def resolve_pagination(self, page: int):
        rendering_page_objects = self.paginator.get_page(page)
        return rendering_page_objects

    def get_view_specific_data(self, request, *args, **kwargs):
        return {'tags': Tag.objects.get_top_tags()}

    def prepare_questions_query(self):
        questions_objects = self.load_questions(
            *self.loader_specific_args,
            **self.loader_specific_kwargs
        )
        self.paginator = Paginator(questions_objects, self.QUESTIONS_PER_PAGE)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        passing_arguments = self.get_view_specific_data(request, *args, **kwargs)
        self.prepare_questions_query()

        page_number = int(request.GET.get('page', 1))
        question_objects = self.resolve_pagination(page_number)

        passing_arguments.update({self.question_objects_template_naming: question_objects})

        return render(
            request,
            self.template,
            passing_arguments
        )


class IndexView(DefaultQuestionsContainPageView):
    template = 'index.html'


class HotQuestionsView(DefaultQuestionsContainPageView):
    template = 'hot.html'
    questions_loader = Question.objects.get_hot
    LIKES_TO_HOT = 10
    loader_specific_args = []
    loader_specific_kwargs = dict(likes_to_hot=LIKES_TO_HOT)


class TagQuestionsView(DefaultQuestionsContainPageView):
    template = 'tag.html'
    questions_loader = Question.objects.get_tagged_question
    loader_specific_args = []
    loader_specific_kwargs = dict()

    def get_view_specific_data(self, request, *args, **kwargs):
        self.loader_specific_kwargs.update({'tag_name': kwargs.get('tag_name')})
        return {'tag_name': kwargs.get('tag_name'), 'tags': Tag.objects.get_top_tags()}


class ConcreteQuestionView(View):
    ANSWERS_PER_PAGE = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paginator = None

    def resolve_pagination(self, page: int):
        rendering_page = self.paginator.get_page(page)
        return rendering_page

    def create_answer_objects(self, question):
        answers = Answer.objects.question_answers(question.pk)
        answers_set = []
        for answer in answers:
            item = {
                'answer': answer,
                'author_avatar': Profile.objects.get_avatar_url(answer.author.pk)
            }
            answers_set.append(item)

        return answers_set

    def prepare_questions_query(self, question):
        # answer_objects = Answer.objects.question_answers(question.pk)
        answer_objects = self.create_answer_objects(question)
        self.paginator = Paginator(answer_objects, self.ANSWERS_PER_PAGE)

    def get(self, request: HttpRequest, question_id) -> HttpResponse:
        question = Question.objects.filter(pk__exact=question_id)[0]
        self.prepare_questions_query(question)
        page_number = int(request.GET.get('page', 1))
        passing_arguments = {'tags': Tag.objects.get_top_tags()}
        passing_arguments.update({'question': load_question_data(question)})
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
