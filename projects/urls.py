from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register ,name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create", views.create_project, name="create"),
    path("details/<int:id>", views.details, name="details"),
    path("edit_links", views.edit_link, name="edit_link"),
    path("edit_todo", views.edit_todo, name="edit_todo"),
    path("complete", views.complete, name="complete"),
    path("reopen", views.reopen, name="reopen"),
    path("save_research", views.save_research, name="save_research"),
    path("my_ToDos", views.checklists, name="checklists")
    
]
