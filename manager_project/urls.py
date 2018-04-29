from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

import manager.views as manager_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', manager_view.CustomLoginView.as_view()),
    url(r'^register/', manager_view.RegisterView.as_view()),
    url(r'^user_list/', manager_view.UserListView.as_view()),
    url(r'^thread_list/', login_required(manager_view.ThreadListView.as_view())),
    url(r'^article_list/', login_required(manager_view.ArticleListView.as_view())),
    url(r'^logout/', manager_view.logout_view),
    # url(r'^worker_list/', login_required(manager_view.WorkerListView.as_view())),
    url(r'^hijack/', include('hijack.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
