import json
import os

from django.shortcuts import render, redirect
from django.urls import reverse

from FinDesk.settings import load_plugin, unload_plugin
from .forms import *
import zipfile
from django.conf import settings
from .utils import *

from django.utils.translation import gettext as _
from django.views.generic import RedirectView, ListView

from django_ledger.models.entity import EntityModel
from django_ledger.views.mixins import LoginRequiredMixIn
from FinDesk.utils.Plugin.models import *


# function based view of all plugins

# def allPlugins_(request):
#     data = {
#         'plugins': Plugin.objects.all()
#     }
#     return render(request, 'allPlugins.html', data)


class allPlugins(LoginRequiredMixIn, ListView):
    template_name = 'allPlugins.html'
    PAGE_TITLE = _('All Plugins')
    context_object_name = 'entities'
    extra_context = {
        'page_title': PAGE_TITLE,
        'header_title': PAGE_TITLE,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_subtitle'] = self.request.user.get_full_name()
        context['header_subtitle_icon'] = 'ei:user'
        context['plugins'] = Plugin.objects.all()
        return context

    def get_queryset(self):
        return EntityModel.objects.for_user(
            user_model=self.request.user
        )


def index(request):
    if request.POST:
        data = load_plugin("Plugin")
        return render(request, 'index.html', {"data": data})
    return render(request, 'index.html')


# def upload_(request):
#     if request.POST:
#         form = PluginForm(request.POST, request.FILES)
#         if form.is_valid():
#             if checkPlugin(form):
#                 plugin = form.save()
#                 with zipfile.ZipFile(plugin.file, 'r') as zip_ref:
#                     filenames = zip_ref.namelist()
#                     zip_ref.extractall(f'{settings.PLUGIN_DIRECTORY}/')
#                     plugin.filename = filenames[0]
#                     config = json.load(open(f'{settings.PLUGIN_DIRECTORY}/{plugin.filename}config.json', 'r'))
#                     plugin.name = config['name']
#                     plugin.author = config['author']
#                     plugin.version = config['version']
#                     plugin.entry = config['entry']
#                     plugin.save()
#                     installPythonDeps(config)
#                     load_plugin(plugin.filename.replace("/", ""))
#                     return redirect(reverse('ledger:home'))
#
#     form = PluginForm()
#     return render(request, 'upload.html', {'form': form})


class upload(LoginRequiredMixIn, ListView):
    template_name = 'upload.html'
    PAGE_TITLE = _('Upload Plugins')
    context_object_name = 'entities'
    extra_context = {
        'page_title': PAGE_TITLE,
        'header_title': PAGE_TITLE,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_subtitle'] = self.request.user.get_full_name()
        context['header_subtitle_icon'] = 'ei:user'
        context['plugins'] = Plugin.objects.all()
        context['form'] = PluginForm()
        return context

    def get_queryset(self):
        return EntityModel.objects.for_user(
            user_model=self.request.user
        )

    def post(self, request, *args, **kwargs):
        form = PluginForm(request.POST, request.FILES)
        if form.is_valid():
            if checkPlugin(form):
                plugin = form.save()
                with zipfile.ZipFile(plugin.file, 'r') as zip_ref:
                    filenames = zip_ref.namelist()
                    zip_ref.extractall(f'{settings.PLUGIN_DIRECTORY}/')
                    plugin.filename = filenames[0]
                    config = json.load(open(f'{settings.PLUGIN_DIRECTORY}/{plugin.filename}config.json', 'r'))
                    plugin.name = config['name']
                    plugin.author = config['author']
                    plugin.version = config['version']
                    plugin.entry = config['entry']
                    plugin.save()
                    installPythonDeps(config)
                    if checkForTemplates(filenames):
                        loadTemplates(plugin)
                    load_plugin(plugin.filename.replace("/", ""))
                    return redirect(reverse('ledger:home'))
        return self.get(request, args, kwargs)


# function based view of toggle enable

# def toggleEnable_(request, id):
#     plugin = Plugin.objects.filter(id=id)
#     if not plugin.count() > 0:
#         return redirect('upload/')
#     plugin = plugin.first()
#     if request.POST:
#         form = EnableForm(request.POST, instance=plugin)
#         if form.is_valid():
#             form.save()
#             toggle = form.cleaned_data.get('active')
#             if not toggle is None:
#                 if toggle:
#                     load_plugin(plugin.filename.replace("/", ""))
#                 else:
#                     name = f'{settings.PLUGIN_DIRECTORY}.' + plugin.filename.replace("/", "")
#                     unload_plugin(name)
#                 return redirect(reverse('ledger:home'))
#
#     data = {
#         'form': EnableForm(instance=plugin)
#     }
#     return render(request, 'enableForm.html', data)


class toggleEnable(LoginRequiredMixIn, ListView):
    template_name = 'enableForm.html'
    PAGE_TITLE = _('Enable/Disable Plugins')
    context_object_name = 'entities'
    extra_context = {
        'page_title': PAGE_TITLE,
        'header_title': PAGE_TITLE,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_subtitle'] = self.request.user.get_full_name()
        context['header_subtitle_icon'] = 'ei:user'
        context['plugins'] = Plugin.objects.all()
        plugin = Plugin.objects.filter(id=self.kwargs.get('id'))
        if not plugin.count() > 0:
            return redirect('upload/')
        plugin = plugin.first()
        context['form'] = EnableForm(instance=plugin)
        context['plugin'] = plugin
        return context

    def get_queryset(self):
        return EntityModel.objects.for_user(
            user_model=self.request.user
        )

    def post(self, request, *args, **kwargs):
        plugin = Plugin.objects.filter(id=self.kwargs.get('id'))
        if not plugin.count() > 0:
            return redirect('upload/')
        plugin = plugin.first()
        form = EnableForm(request.POST, instance=plugin)
        if form.is_valid():
            form.save()
            toggle = form.cleaned_data.get('active')
            if not toggle is None:
                if toggle:
                    load_plugin(plugin.filename.replace("/", ""))
                else:
                    name = f'{settings.PLUGIN_DIRECTORY}.' + plugin.filename.replace("/", "")
                    unload_plugin(name)
                return redirect(reverse('ledger:home'))
