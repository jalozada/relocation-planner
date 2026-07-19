from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.ProjectListView.as_view(), name="project-list"),
    path("projects/new/", views.ProjectCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project-delete"),
    path("projects/<int:project_pk>/people/", views.PersonListView.as_view(), name="person-list"),
    path("projects/<int:project_pk>/people/new/", views.PersonCreateView.as_view(), name="person-create"),
    path("people/<int:pk>/", views.PersonDetailView.as_view(), name="person-detail"),
    path("people/<int:pk>/edit/", views.PersonUpdateView.as_view(), name="person-update"),
    path("people/<int:pk>/delete/", views.PersonDeleteView.as_view(), name="person-delete"),
    path("projects/<int:project_pk>/documents/", views.DocumentListView.as_view(), name="document-list"),
    path("projects/<int:project_pk>/documents/new/", views.DocumentCreateView.as_view(), name="document-create"),
    path("documents/<int:pk>/", views.DocumentDetailView.as_view(), name="document-detail"),
    path("documents/<int:pk>/edit/", views.DocumentUpdateView.as_view(), name="document-update"),
    path("documents/<int:pk>/delete/", views.DocumentDeleteView.as_view(), name="document-delete"),
    path("projects/<int:project_pk>/milestones/", views.MilestoneListView.as_view(), name="milestone-list"),
    path("projects/<int:project_pk>/milestones/new/", views.MilestoneCreateView.as_view(), name="milestone-create"),
    path("milestones/<int:pk>/", views.MilestoneDetailView.as_view(), name="milestone-detail"),
    path("milestones/<int:pk>/edit/", views.MilestoneUpdateView.as_view(), name="milestone-update"),
    path("milestones/<int:pk>/delete/", views.MilestoneDeleteView.as_view(), name="milestone-delete"),
    path("projects/<int:project_pk>/tasks/", views.TaskListView.as_view(), name="task-list"),
    path("projects/<int:project_pk>/tasks/new/", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
]
