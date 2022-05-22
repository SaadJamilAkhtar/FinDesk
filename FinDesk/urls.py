"""FinDesk URL Configuration

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
from django.dispatch import receiver
from django.urls import path, include
from FinDesk.utils.Plugin.views import *
from FinDesk.utils.Plugin.utils import *
from django.conf import settings

from FinDesk.settings import plugin_loaded, plugin_unloaded

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_ledger.urls', namespace='ledger')),
    path('upload', upload.as_view(), name='upload-plugin'),
    path('all/', allPlugins.as_view(), name='all-plugins'),
    path('plugin/<int:id>', toggleEnable.as_view(), name='toggle'),
]


@receiver(plugin_loaded)
def load_urls(sender, **kwargs):
    try:
        print("adding")
        urlpatterns.append(
            path(str(sender).lower() + "/",
                 include((settings.PLUGIN_DIRECTORY + "." + str(sender) + ".urls", sender), namespace=sender),
                 ))
    except Exception as e:
        print(e)
        pass


@receiver(plugin_unloaded)
def unload_urls(sender, **kwargs):
    for url in urlpatterns:
        print(f"{str(url.pattern)} : {(str(sender).lower() + '/')}")
        if str(url.pattern).strip() == (str(sender).lower() + "/"):
            urlpatterns.remove(url)


try:
    mountPlugins()
except:
    pass
