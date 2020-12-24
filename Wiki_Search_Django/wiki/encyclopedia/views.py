from django.shortcuts import render
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
from django.contrib import messages
import secrets

class NewTaskForm(forms.Form):
    title = forms.CharField()
    textarea = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def newpage(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            textarea = form.cleaned_data['textarea']
            if title in util.list_entries():
                messages.error(request,'The entry already exists')
            else:
                util.save_entry(title, textarea)
                return HttpResponseRedirect(reverse("click:index"))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form":form,
            })
    return render(request, "encyclopedia/newpage.html", {
        "form": NewTaskForm(),
    })

def entry(request, title):
    all_titles = util.list_entries()
    if title in all_titles:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "textarea": markdown2.markdown(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    search = request.GET.get('q','')
    all_titles = util.list_entries()
    sub_str_list = []
    if search in [x.lower() for x in all_titles]:
        return render(request, "encyclopedia/entry.html", {
        "title": search,
        "textarea": markdown2.markdown(util.get_entry(search))
    })
    else:
        for title in all_titles:
            if search.lower() in title.lower():
                sub_str_list.append(title)
        return render(request, "encyclopedia/search.html", {
            "sub_str_list": sub_str_list
        })
    return HttpResponseRedirect(reverse("click:index"))

def random(request):
    titles = util.list_entries()
    random_title = secrets.choice(titles)
    return render(request, "encyclopedia/entry.html", {
        "title": random_title,
        "textarea": markdown2.markdown(util.get_entry(random_title))
    })

def edit(request, editPage):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data['textarea']
            util.save_entry(editPage, textarea)
            return render(request, "encyclopedia/entry.html", {
                "title": editPage,
                "textarea": markdown2.markdown(util.get_entry(editPage))
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "title_ph":"",
                "text_ph" :""
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            "title_ph": editPage,
            "text_ph" : util.get_entry(editPage)
        })


    
