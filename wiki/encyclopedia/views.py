from django.shortcuts import render
from django import forms
from django.contrib import messages
from . import util
import os

class createForm(forms.Form):
    title = forms.CharField(label="entryTitle")
    text = forms.CharField(label="entryText")
def index(request):
    if request.GET.get('q') is not None:
        query = request.GET.get('q')
        if util.get_entry(query):
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "body": util.get_entry(query)
            })
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                if query.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/index.html", {
                "entries": results
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, name):
    if util.get_entry(name):
        return render(request, "encyclopedia/entry.html", {
            "title": name,
            "body": util.get_entry(name)
        })
    else:
        return render(request, 'encyclopedia/index.html', {
            "entries": util.list_entries(),
            "message": "Invalid URL"
        })

def create(request):
    if request.method == "POST":
        title = request.POST.get('entryTitle')
        text = request.POST.get('entryText')

        if util.get_entry(title):
            return render(request, 'encyclopedia/create.html', {
                "message": "Page already created",
                "type": "danger",
                "alertTitle": "Error!"
            })
        
        else:
            directory = 'entries'
            filename = title + '.md'

            full_path = os.path.join(directory, filename)

            f = open(full_path, 'w')
            f.write(text)
            f.close()
            return render(request, 'encyclopedia/create.html', {
                "message": "Page created!",
                "type": "success",
                "alertTitle": "Success!"
            })
    return render(request, 'encyclopedia/create.html')
    

