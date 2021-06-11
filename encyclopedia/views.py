from django.shortcuts import render
from django import forms

from . import util

import markdown2
import random

import encyclopedia
        
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# function that opens the page with title "Title"
def openpage(request, Title):
    site_md = util.get_entry(Title)
    if (site_md != None):
        site_html = markdown2.markdown(site_md)
    else:
        site_html = "None"
    return render(request, "encyclopedia/title.html", {
        "Title": Title,
        "site": site_html,
        "md":site_md
    })

def search(request):
    if request.method == "POST":
        form = request.POST
        query = form["q"]

        #check if query matches any existing entry
        if util.get_entry(query) != None:
            return openpage(request, query)
        else:
            results = []
            for entry in util.list_entries():
                if (query in entry) or (query.capitalize() in entry):
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "results": results
            })

def newpage(request):
    error = 0
    title = ""
    if request.method == "POST":
        form = request.POST
        title = form["newtitle"]
        content = form["newcontent"]
        for entry in util.list_entries():
            if title == entry:
                error = 1
                break
        if (error == 1):
            return render(request, "encyclopedia/newpage.html", {
                "errorcode": error,
                "title": title,
            })
        elif (error == 0):
            util.save_entry(title, content)
            return openpage(request, title)
    return render(request, "encyclopedia/newpage.html", {
        "errorcode": error,
        "title": title,
    })

def editpage(request):
    if request.method == "POST":
        form = request.POST
        if (form["f_editing"] == "no"):
            title = form["title"]
            content = form["content"]
            return render(request, "encyclopedia/editpage.html", {
                "title": title,
                "content": content
            })
        elif (form["f_editing"] == "yes"):
            title = form["title"]
            content = form["editedcontent"]
            util.save_entry(title, content)
            return openpage(request, title)

def randompage(request):
    page = util.list_entries()[random.randint(0, len(util.list_entries())-1)]
    return openpage(request, page)