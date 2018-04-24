from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.views import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
import datetime
import logging

from manager.models import *
from manager.forms import *


class CustomLoginView(TemplateView):
    template_name = "login.html"

    def get(self, _, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_next_redirect_url())
        else:
            kwargs = {'template_name': 'login.html'}
            return login(self.request, *args, **kwargs)

    def post(self, _, *args, **kwargs):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.get_next_redirect_url())
        else:
            kwargs = {'template_name': 'login.html'}
            return login(self.request, *args, **kwargs)

    def get_next_redirect_url(self):
        redirect_url = self.request.GET.get('next')
        if not redirect_url or redirect_url == '/':
            redirect_url = '/article_list/'
        return redirect_url


class RegisterView(TemplateView):
    template_name = "register.html"

    def get(self, request, *args, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        return render(self.request, self.template_name, context)

    def post(self, _, *args, **kwargs):
        identifier = self.request.POST['identifier']
        name = self.request.POST['name']
        password = self.request.POST['password']

        form = RegisterForm(self.request.POST)
        if form.is_valid():
            person = Person(identifier=identifier, name=name, is_superuser=False)
            person.set_password(password)
            person.save()

            return redirect('/user_list/')
        else:
            context = super(RegisterView, self).get_context_data(**kwargs)
            context['form'] = form
            return render(self.request, self.template_name, context)



class UserListView(TemplateView):
	template_name = "user_list.html"

	def get(self, request, *args, **kwargs):
		context = super(UserListView, self).get_context_data(**kwargs)
		persons = Person.objects.all()
		context['persons'] = persons
		return render(self.request, self.template_name, context)

class ArticleListView(TemplateView):
    template_name = "article_list.html"

    def get(self, request, *args, **kwargs):
        info(request.GET.get("thread_id"))
        person = Person.objects.get(pk=self.request.user.id)
        context = super(ArticleListView, self).get_context_data(**kwargs)
        articles = Article.objects.all()
        context['articles'] = articles
        context['thread_id'] = request.GET.get("thread_id")
        return render(self.request, self.template_name, context)

    def post(self, _, *args, **kwargs):
        person = Person.objects.get(pk=self.request.user.id)
        thread = Thread.objects.get(pk=self.request.POST['thread_id'])
        title = self.request.POST['title']
        text = self.request.POST['text']
        Article.objects.create(person=person, thread=thread, title=title, text=text, insymd=datetime.datetime.today())

        return redirect('/article_list/?thread_id=' + str(thread.id))

class ThreadListView(TemplateView):
    template_name = "thread_list.html"

    def get(self, request, *args, **kwargs):
        context = super(ThreadListView, self).get_context_data(**kwargs)
        threads = Thread.objects.all()
        context['threads'] = threads
        return render(self.request, self.template_name, context)

    def post(self, _, *args, **kwargs):
        title = self.request.POST['title']
        insymd = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Thread.objects.create(title=title, insymd=insymd)

        return redirect('/thread_list/')



def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

def info(msg):
    logger = logging.getLogger('command')
    logger.info(msg)
