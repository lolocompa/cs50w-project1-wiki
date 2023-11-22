from django.shortcuts import redirect, render
import markdown
import random

from . import util


def convert_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if not content:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "message": "All Pages",
        "entries": util.list_entries()
    })


def entry(request, title):
    html = convert_html(title)
    if html is None:
        return render(request, "encyclopedia/error.html", {
            "message": "entry not found" 
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })
    

def search(request):
    recomended = []
    if request.method == "POST":
        search = request.POST["q"]
        search = str(search).lower()
        content = util.list_entries()
        for element in content:
            if element.lower() == search:
                return redirect(f"wiki/{search}")
        for element2 in content:
            if search in element2.lower():
                recomended.append(element2)
        if recomended:
            return render(request, "encyclopedia/index.html", {
                "message": "recomended pages",
                "entries": recomended
            })
        else:            
            return render(request, "encyclopedia/error.html", {
                "message": "error, no results found"
            })
        



def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        title_check = str(title).lower()
        mark = request.POST["markdown"]
        content = util.list_entries()
        for element in content:
            if element.lower() == title_check:
                return render(request, "encyclopedia/error.html", {
                    "message": "page already exists"
                })
        util.save_entry(title, mark)
        convert =  convert_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": convert
        })
    else:
        return render(request, "encyclopedia/new_page.html")    
    



def edit_page(request):
    if request.method == "GET":
        title = request.GET.get("title")
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html",{
            "content": content,
            "title": title
        })
    else:
        title = request.POST["title"]
        edit = request.POST["edit"]
        util.save_entry(title, edit)
        convert =  convert_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": convert
        })



def random_entry(request):
    content = util.list_entries()
    length = len(content)
    random_number = random.randint(0, length - 1)
    random_entry = content[random_number]
    html = convert_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html
    })
