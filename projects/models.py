from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Project(models.Model):
    project_name = models.CharField(max_length=64)
    user = models.ForeignKey(User, related_name="user_projects", on_delete=models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()
    project_class = models.CharField(max_length=64)
    status = models.CharField(default="Incomplete", max_length=20, choices=[
        ("Incomplete", "Incomplete"), 
        ("Complete", "Complete")
    ])
    def __str__(self):
        return f"{self.project_name} by {self.user}"


class Link(models.Model):
    link_tag = models.CharField(max_length=64)
    link_type = models.CharField(max_length=64, choices=[
        ("Document", "Document"),
        ("Research", "Research")
    ])
    url = models.URLField(blank=True, null=True)
    link_status = models.CharField(default="Uncited", max_length=64, choices=[
        ("Uncited", "Uncited"),
        ("Cited", "Cited")
    ])
    doc_status = models.CharField(default="Incomplete", max_length=64, choices=[
        ("Incomplete", "Incomplete"),
        ("Complete", "Complete")
    ])
    due_date = models.DateField(null=True, blank=True)
    doc_file = models.FileField(blank=True, null=True)
    user = models.ForeignKey(User, related_name="user_links", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_links")
    
    def __str__(self):
        return f"'{self.link_tag}' for {self.project} by {self.user}"

class ToDo(models.Model):
    item = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"'{self.id}: {self.user}'s toDo for {self.project}: {self.item}"
