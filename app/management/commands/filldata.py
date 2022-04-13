from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Like, Tag
from django.contrib.auth.models import User
from django.utils.timezone import timezone

import requests
import random
import datetime


class Command(BaseCommand):
    RANDOM_API_KEY = '78c7df1074544d209e549dc135589056'
    RANDOM_TEXT_API = 'https://randommer.io/api/Text/LoremIpsum'
    RANDOM_NAME_API = 'https://randommer.io/api/Name'
    PARAGRAPHS_AMOUNT = 1

    SCALE = 100
    USERS_NEEDS = 10000 // SCALE
    QUESTIONS_NEEDS = 100000 // SCALE
    ANSWERS_NEEDS = 1000000 // SCALE
    TAGS_NEEDS = 20000 * QUESTIONS_NEEDS // SCALE
    LIKES_NEEDS = 2000000 // SCALE

    TITLE_LEN = 10
    MIN_TEXT_LEN = 20
    MAX_TEXT_LEN = 100
    MAX_ANSWERS = 5
    MAX_TAGS = 5
    MAX_LIKES = 40

    def __init__(self):
        super().__init__()
        self.text_dataset = self.generate_words_dataset()
        self.names_set = self.generate_names_set()

    def generate_words_dataset(self):
        params = {'loremType': 'normal', 'type': 'paragraphs', 'number': self.PARAGRAPHS_AMOUNT}
        r = requests.get(
            self.RANDOM_TEXT_API,
            params=params,
            headers={'X-Api-Key': self.RANDOM_API_KEY}
        )
        return r.text.split()

    def generate_names_set(self):
        params = {'nameType': 'fullname', 'quantity': 100}
        r = requests.get(
            self.RANDOM_NAME_API,
            params=params,
            headers={'X-Api-Key': self.RANDOM_API_KEY}
        )
        return r.json()

    def create_text_by_word_length(self, len):
        result_string = str()
        for i in range(len):
            result_string = result_string + random.choice(self.text_dataset) + ' '
        return result_string

    def create_users_and_ref_profiles(self):
        def create_user(user_counter):
            name_choice = f'{random.choice(self.names_set)}{user_counter}'
            name_split = name_choice.split()
            pwd = f'{random.choice(self.text_dataset)}{random.choice(self.text_dataset)}{random.choice(self.text_dataset)}'
            user_dict_repr = {
                'username': name_choice,
                'first_name': name_split[0],
                'last_name': name_split[1],
                'password': pwd,
                'email': f'{random.choice(self.text_dataset)}@domen.mail',
                'is_staff': False,
                'is_active': True,
                'is_superuser': False,
                'last_login': datetime.datetime.now(tz=timezone.utc),
                'date_joined': datetime.date.today()
            }
            return user_dict_repr

        users_set = []
        profiles_set = []
        for i in range(self.USERS_NEEDS):
            user = User(**create_user(i))
            user.save()
            users_set.append(user)
            profile = Profile(user=user)
            profiles_set.append(profile)

        Profile.objects.bulk_create(profiles_set)

    def create_questions(self, users):
        def create_question(user):
            question_fields = {
                'title': self.create_text_by_word_length(self.TITLE_LEN),
                'text': self.create_text_by_word_length(random.randint(self.MIN_TEXT_LEN, self.MAX_TEXT_LEN)),
                'time': datetime.datetime.now(tz=timezone.utc),
                'author': user
            }
            return question_fields

        questions_set = []
        for i in range(self.QUESTIONS_NEEDS):
            question = Question(**create_question(random.choice(users)))
            questions_set.append(question)

        Question.objects.bulk_create(questions_set)

    def create_answers(self, users, questions):
        def create_answer(user, question):
            answer_fields = {
                'text': self.create_text_by_word_length(random.randint(self.MIN_TEXT_LEN, self.MAX_TEXT_LEN)),
                'correct': random.choice([True, False]),
                'time': datetime.datetime.now(tz=timezone.utc),
                'question': question,
                'author': user
            }
            return answer_fields

        answers_created_indicate = self.ANSWERS_NEEDS
        answers_set = []
        while answers_created_indicate > 0:
            one_question_answers_count = random.randint(0, self.MAX_ANSWERS)
            answers_created_indicate -= one_question_answers_count
            question = random.choice(questions)
            for i in range(one_question_answers_count):
                answer = Answer(**create_answer(random.choice(users), question))
                answers_set.append(answer)

        Answer.objects.bulk_create(answers_set)

    def create_tags(self, questions):
        def create_tag(question):
            tag_fields = {
                'tag_name': random.choice(self.text_dataset),
                'question': question
            }
            return tag_fields

        tags_created_indicate = self.TAGS_NEEDS
        tags_set = []
        while tags_created_indicate > 0:
            one_question_tags_amount = random.randint(0, self.MAX_TAGS)
            tags_created_indicate -= one_question_tags_amount
            question = random.choice(questions)
            for i in range(one_question_tags_amount):
                tag = Tag(**create_tag(question))
                tags_set.append(tag)

        Tag.objects.bulk_create(tags_set)

    def create_likes(self, users, questions):
        def create_like(user, question):
            like_fields = {
                'user': user,
                'question': question
            }
            return like_fields

        likes_created_indicate = self.LIKES_NEEDS
        likes_set = []
        while likes_created_indicate > 0:
            one_question_like_amount = random.randint(0, self.MAX_LIKES)
            likes_created_indicate -= one_question_like_amount
            question = random.choice(questions)
            for i in range(one_question_like_amount):
                like = Like(**create_like(random.choice(users), question))
                likes_set.append(like)

        Like.objects.bulk_create(likes_set)

    def handle(self, *args, **options):
        self.create_users_and_ref_profiles()
        users = User.objects.all()
        self.create_questions(users)
        questions = Question.objects.all()
        self.create_answers(users, questions)
        self.create_tags(questions)
        self.create_likes(users, questions)
        self.stdout.write(self.style.SUCCESS('SUCCESS'))
