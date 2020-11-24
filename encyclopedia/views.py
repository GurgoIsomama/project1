from encyclopedia.util import get_entry, save_entry
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
from . import util
from markdown2 import Markdown
import os, random

import encyclopedia

md = Markdown()

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea,label="Enter Markdowncontent Below")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    obj = util.get_entry(title)
    if not obj:
        return render(request, "encyclopedia/entry.html", {
            "entry": None,
            "title" : title,
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": md.convert(obj),
            "title": title,
        })

def search(request):
    if request.method =="GET":
        search = f"{request.GET.get('q')}"
        entries = util.list_entries()
        search_results = []
        for filename in entries: 
            if filename==search:
                return entry(request, search)
            elif search in filename:
                search_results.append(filename)
        return render(request, "encyclopedia/search.html", {
        "search_results" : search_results,
        "search" : search
        })
    else:        
        return render(request, "encyclopedia/search.html", {
            "search" : "method in search.html != GET "
        })

def add(request):
    if request.method == "POST":
            form = NewPageForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                obj = util.get_entry(title)
                if not obj:
                    save_entry(title, content)
                    return entry(request, title)
                else:
                   return render(request, "encyclopedia/add.html", {
                    "form": form,
                    "error": True,
                }) 
            else:
                return render(request, "encyclopedia/add.html", {
                    "form": form
                })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewPageForm()
        })


def random_page(request):
    entries = util.list_entries() 
    filename = random.choice(entries)
    return entry(request, filename)

