from encyclopedia.util import get_entry
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
from . import util
from markdown2 import Markdown

md = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": md.convert(util.get_entry(title)),
        "title": title,
    })


# def add(request):
