from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.views import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
import datetime
import logging

from manager.models import *


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
            redirect_url = '/worker_list/'
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
		email = self.request.POST['email']
		year = self.request.POST['birth_year']
		month = self.request.POST['birth_month']
		day = self.request.POST['birth_day']
		sex = self.request.POST['sex']
		address_from = self.request.POST['address_from']
		current_address = self.request.POST['current_address']

		person = Person(identifier=identifier, name=name, email=email, birthday=datetime.datetime(int(year), int(month), int(day)), sex=int(sex), address_from=int(address_from), current_address=int(current_address), is_superuser=False)
		person.set_password(password)
		person.save()

		return redirect('/user_list/')

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
        info(self.request.user.id)
        person = Person.objects.get(pk=self.request.user.id)
        context = super(ArticleListView, self).get_context_data(**kwargs)
        articles = Article.objects.all()
        context['articles'] = articles
        return render(self.request, self.template_name, context)

    def post(self, _, *args, **kwargs):
        person = Person.objects.get(pk=self.request.user.id)
        title = self.request.POST['title']
        text = self.request.POST['text']
        Article.objects.create(person=person, title=title, text=text, insymd=datetime.datetime.today())

        return redirect('/article_list/')


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

def info(msg):
    logger = logging.getLogger('command')
    logger.info(msg)
