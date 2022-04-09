from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Like, Tag
from django.contrib.auth.models import User
from django.utils.timezone import timezone

import requests
import random
import datetime


class Command(BaseCommand):
    help = 'Test command'
    RANDOM_API_KEY = '78c7df1074544d209e549dc135589056'
    RANDOM_TEXT_APY = 'https://randommer.io/api/Text/LoremIpsum'
    RANDOM_NAME_API = 'https://randommer.io/api/Name'
    PARAGRAPHS_AMOUNT = 10

    SCALE = 5000
    USERS_NEEDS = 10000 // SCALE
    QUESTIONS_NEEDS = 100000 // SCALE
    ANSWERS_NEEDS = 1000000 // SCALE
    TAGS_NEEDS = 10000 // SCALE
    LIKES_NEEDS = 2000000 // SCALE

    def __init__(self):
        super().__init__()
        self.text_dataset = self.generate_words_dataset()
        self.names_set = self.generate_names_set()
        self.users_set = []
        self.profiles_set = []

    def generate_words_dataset(self):
        params = {'loremType': 'normal', 'type': 'paragraphs', 'number': self.PARAGRAPHS_AMOUNT}
        r = requests.get(
            self.RANDOM_TEXT_APY,
            params=params,
            headers={'X-Api-Key': self.RANDOM_API_KEY}
        )
        return r.text.split()

    def generate_names_set(self):
        params = {'nameType': 'fullname', 'quantity': 1000}
        r = requests.get(
            self.RANDOM_NAME_API,
            params=params,
            headers={'X-Api-Key': self.RANDOM_API_KEY}
        )
        return r.json()

    used_names = {}

    def create_user(self):
        name_choice = random.choice(self.names_set)
        while name_choice in self.used_names:
            name_choice = random.choice(self.names_set)
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

    def create_users_and_ref_profiles(self):
        self.users_set = []
        self.profiles_set = []
        for i in range(self.USERS_NEEDS):
            user = User(**self.create_user())
            user.save()
            profile = Profile(user=user)
            self.profiles_set.append(profile)

        Profile.objects.bulk_create(self.profiles_set)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('FIRST COMMAND MESSAGE'))
        self.create_users_and_ref_profiles()
        # self.create_profiles()
