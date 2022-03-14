import json
import os

from django.shortcuts import render, redirect
from django.urls import reverse

from FinDesk.settings import load_plugin, unload_plugin
from .forms import *
import zipfile
from django.conf import settings
from .utils import *


def index(request):
    if request.POST:
        data = load_plugin("Plugin")
        return render(request, 'index.html', {"data": data})
    return render(request, 'index.html')


def upload(request):
    if request.POST:
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
                    print(plugin.getEntryPoint())
                    installPythonDeps(config)
                    load_plugin(plugin.filename.replace("/", ""))
                    return redirect(reverse('ledger:home'))

    form = PluginForm()
    return render(request, 'upload.html', {'form': form})


def allPlugins(request):
    data = {
        'plugins': Plugin.objects.all()
    }
    return render(request, 'allPlugins.html', data)


def toggleEnable(request, id):
    plugin = Plugin.objects.filter(id=id)
    if not plugin.count() > 0:
        return redirect('upload/')
    plugin = plugin.first()
    if request.POST:
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

    data = {
        'form': EnableForm(instance=plugin)
    }
    return render(request, 'enableForm.html', data)
