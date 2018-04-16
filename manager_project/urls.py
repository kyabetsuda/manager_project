from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

import manager.views as manager_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^worker_list/', manager_view.WorkerListView.as_view())
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
