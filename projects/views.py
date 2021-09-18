import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Project, Link, ToDo

# Create your views here.
def index(request):
    projects = Project.objects.filter(user=request.user).order_by("-status")
    for project in projects:
        project.due_date = project.due_date.strftime("%Y-%m-%d")
    return render(request, "projects/index.html", {
        "projects": projects
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "projects/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "projects/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "projects/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "projects/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "projects/register.html")


@csrf_exempt
def create_project(request):
    if request.method !="POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    project_name = data.get("name")
    project_class = data.get("class")
    due_date = data.get("due")
    start_date = datetime.date.today()
    project = Project(project_name=project_name, user=request.user, start_date=start_date, due_date=due_date, project_class=project_class)
    project.save()
    return JsonResponse({"id": project.id}, status=201)


def details(request, id):
    project = Project.objects.get(id=id)
    user_projects=Project.objects.exclude(id=id).filter(user=request.user, status="Incomplete")
    research_links = Link.objects.filter(user=request.user, project=project, link_type="Research")
    uncited = len(Link.objects.filter(user=request.user, project=project, link_type="Research", link_status="Uncited"))
    incomplete = len(Link.objects.filter(user=request.user, project=project, link_type="Document",doc_status="Incomplete"))
    doc_links = Link.objects.filter(user=request.user, project=project, link_type="Document")
    toDos = ToDo.objects.filter(user=request.user, project=project).order_by("completed")
    not_done = len(ToDo.objects.filter(user=request.user,project=project,completed=False))
    deltaDays = project.due_date - datetime.date.today()
    return render(request, "projects/details.html", {
        "project":project,
        "research_links": research_links,
        "all_projects": user_projects,
        "doc_links": doc_links,
        "toDos": toDos,
        "days_left": deltaDays.days,
        "uncited": uncited,
        "incomplete": incomplete,
        "not_done":not_done
    })
    
@csrf_exempt
@login_required
def edit_link(request):
    user = request.user
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    link_id = data.get("link_id")
    request = data.get("action")
    if request == "Remove":
        link = Link.objects.get(id=link_id)
        link.delete()
        return JsonResponse({"message": "Link removed successfully"}, status=204)
    else: 
        link_type = data.get("type")
        if link_type == "Research":
            project = Project.objects.get(id=data.get("project"))
            link_tag = data.get("tag")
            url = data.get("url")
            new_link = Link(project=project, user=user, link_tag=link_tag, url=url, link_type="Research")
            new_link.save()
            return JsonResponse({"message": "Link added successfully"}, status=201)
        if link_type == "Document":
            if data.get("input") == "link":
                print("here")
                project = Project.objects.get(id=data.get("project"))
                link_tag = data.get("tag")
                url = data.get("url")
                new_link = Link(project=project, user=user, link_tag=link_tag, url=url, link_type="Document")
                new_link.save()
                return JsonResponse({"message": "Link added successfully"}, status=201)
            else:
                project = Project.objects.get(id=data.get("project"))
                link_tag = data.get("tag")
                doc_file = data.get("file")
                print("hello")
                new_link = Link(project=project, user=user, link_tag=link_tag, doc_file=doc_file, link_type="Document")
                new_link.save()
                return JsonResponse({"message": "Link added successfully"}, status=201)

@csrf_exempt
def edit_todo(request):
    user = request.user
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    if data.get("action") == "add":
        item = data.get("item")
        project = Project.objects.get(id=data.get("project"))
        todo = ToDo(user=user, project=project, item=item)
        todo.save()
        return JsonResponse({"id": todo.id}, status=201)
    elif data.get("action") == "complete":
        todo = ToDo.objects.get(id=data.get("todo"))
        todo.completed = True
        todo.save()
        return JsonResponse({"message": "ToDo updated successfully"}, status=200)
    elif data.get("action") == "delete":
        todo = ToDo.objects.get(id=data.get("todo"))
        todo.delete()
        return JsonResponse({"message": "ToDo deleted successfully"}, status=204)
    else:
        todo = ToDo.objects.get(id=data.get("todo"))
        todo.completed = False
        todo.save()
        return JsonResponse({"message": "ToDo updated successfully"}, status=200)

@csrf_exempt
def complete(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    project= Project.objects.get(id=data.get("project"))
    project.status = "Complete"
    project.save()
    return JsonResponse({"message": "Project updated successfully"}, status=200)
    
@csrf_exempt
def reopen(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    project= Project.objects.get(id=data.get("project"))
    project.status = "Incomplete"
    project.save()
    return JsonResponse({"message": "Project updated successfully"}, status=200)

@csrf_exempt
def save_research(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    link= Link.objects.get(id=data.get("link"))
    if data.get("type") == "research":
        if link.link_status == "Uncited":    
            link.link_status = "Cited"
            link.save()
        else:
            link.link_status = "Uncited"
            link.save()
    else:
        if link.doc_status == "Complete":
            link.doc_status = "Incomplete"
            link.save()
        else:
            link.doc_status = "Complete"
            link.save()
    return JsonResponse({"message": "Changes saved successfully"}, status=200)

def checklists(request):
    user=request.user
    projects = Project.objects.filter(user=request.user,status="Incomplete")
    checks = ToDo.objects.filter(user=user).order_by("completed")
    return render(request, "projects/lists.html", {
        "projects":projects,
        "todos": checks
    })