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
        context = super(ArticleListView, self).get_context_data(**kwargs)

        # もしthread_idかpageが存在しなければ
        if request.GET.get("thread_id") == "" or request.GET.get("thread_id") is None or request.GET.get("page") == "" or request.GET.get("page") is None:
            return redirect('/error/')

        # ページ番号
        page = int(request.GET.get("page"))
        # まずは全ての記事を取得
        articles = Article.objects.filter(thread__id=request.GET.get("thread_id"))

        # もし存在しないページ数を開いたら
        if len(articles) <= (page-1)*5:
            return redirect('/error/')
        # 次のページ、最後のページ制御
        context['start'] = True
        context['end'] = True
        # 最初のページの場合
        if page == 1:
            context['start'] = False;
        # 最後のページの場合
        elif (len(articles) // (page*5)) <= 0:
            context['end'] = False
        # ページ番号挿入
        # もし記事数が25(5*5に満たない場合)
        if len(articles)//5 < 5:
            numbers = []
            for i in range(len(articles)//5+1):
                numbers.append(i+1)


        # 次に表示する記事文だけ取得
        articles = Article.objects.filter(thread__id=request.GET.get("thread_id"))[(page-1)*5:(page-1+1)*5]

        info(len(articles) // 5)
        context['articles'] = articles
        # thread_id埋め込み
        context['thread_id'] = request.GET.get("thread_id")
        # ページ番号埋め込み
        context['page'] = request.GET.get("page")
        # ページ数挿入
        context['numbers'] = numbers
        return render(self.request, self.template_name, context)

    def post(self, _, *args, **kwargs):
        person = Person.objects.get(pk=self.request.user.id)
        thread = Thread.objects.get(pk=self.request.POST['thread_id'])
        # ページ番号取得
        page = self.request.POST['page']
        title = self.request.POST['title']
        text = self.request.POST['text']
        Article.objects.create(person=person, thread=thread, title=title, text=text, insymd=datetime.datetime.today())

        return redirect('/article_list/?thread_id=' + str(thread.id) + "&page=" + page)

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
