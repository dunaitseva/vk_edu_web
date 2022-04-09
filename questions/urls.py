"""questions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index-view'),
    path('hot/', views.HotQuestionsView.as_view(), name='hot-view'),
    path('question/<int:question_id>', views.QuestionView.as_view(), name='question-view'),
    path('tag/<str:tag_name>/', views.TagQuestionsView.as_view(), name='tag-view'),
    path('login/', views.LoginView.as_view(), name='login-view'),
    path('signup/', views.RegisterView.as_view(), name='register-view'),
    path('ask/', views.AskView.as_view(), name='ask-view'),
    path('settings/', views.SettingsView.as_view(), name='settings-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
