from django.db import models
from django.contrib.auth.models import User
from questions.settings import MEDIA_ROOT


# Create your models here.
class ProfileManager(models.Manager):
    def get_avatar(self, user_id):
        return Profile.objects.filter(user__pk=user_id)[0].avatar


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='common_avatar.png')

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}"


class QuestionsManager(models.Manager):
    def get_hot(self, likes_to_hot):
        result_query = []
        questions = Question.objects.all()
        for question in questions:
            if Like.objects.count_question_likes(question.pk) >= likes_to_hot:
                result_query.append(question)

        return result_query

    def get_tagged_question(self, tag_name):
        tags_objects = Tag.objects.filter(tag_name__exact=tag_name)
        result_query = []
        for tags_object in tags_objects:
            result_query.append(tags_object.question)
        return result_query


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = QuestionsManager()

    def __str__(self):
        return f"{self.author.username} {self.title}"


class AnswerManager(models.Manager):
    def count_question_answers(self, question_id):
        return Answer.objects.filter(question__pk=question_id).count()

    def question_answers(self, question_id):
        return Answer.objects.filter(question__pk=question_id)


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = AnswerManager()

    def __str__(self):
        return f"{self.author.username} {self.question.title}"


class LikeManager(models.Manager):
    def count_question_likes(self, question_id):
        return Like.objects.filter(question__pk=question_id).count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = LikeManager()

    def __str__(self):
        return f"{self.user.username} {self.question.title}"


class TagManager(models.Manager):
    def question_tags(self, question_id):
        return Tag.objects.filter(question__pk=question_id)


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = TagManager()

    def __str__(self):
        return f"{self.tag_name} {self.question.title}"
