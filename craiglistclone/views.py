from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def home(request):
    return render(request, "base.html")


def new_search(request):
    search = request.POST.get("search")
    # print(search)
    staff_for_frontend = {"search": search}
    return render(request, "craiglistclone/new_search.html", staff_for_frontend)


# Create your views here.
