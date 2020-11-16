from django.shortcuts import render
from django.http import HttpResponseRedirect
from random import randrange
from django import forms
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    for n in util.list_entries():
        if n == title:
            break
        elif n.lower() == title.lower():
            return HttpResponseRedirect(f'/wiki/{n}')
    content = util.get_entry(title)
    if content:
        content = markdown2.markdown(content)
    return render(request, 'encyclopedia/entry.html', {
        'entry': content,
        'title': title
    })


def search(request):
    keyword = request.GET['q']
    results = []
    for n in util.list_entries():
        if n.lower() == keyword.lower():
            return HttpResponseRedirect(f'/wiki/{n}')
        elif n.lower().find(keyword.lower()) >= 0:
            results.append(n)
    return render(request, 'encyclopedia/search.html', {
        'keyword': keyword,
        'results': results
    })


def new_entry(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        list = [x.lower() for x in util.list_entries()]
        if title.lower() in list:
            return render(request, 'encyclopedia/new.html', {'title': title, 'content': content, 'invalid': True})
        else:
            util.save_entry(title.strip(), content)
            return HttpResponseRedirect(f'/wiki/{title}')

    return render(request, 'encyclopedia/new.html')


def edit_entry(request, title):
    if request.method == 'POST':
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(f'/wiki/{title}')

    if title in util.list_entries():
        return render(request, 'encyclopedia/edit.html', {'title': title, 'content': util.get_entry(title)})
    else:
        return render(request, 'encyclopedia/entry.html', {
            'entry': None,
            'title': title
        })


def random(request):
    list = util.list_entries()
    item = list[randrange(len(list))]
    return HttpResponseRedirect(f'/wiki/{item}')
