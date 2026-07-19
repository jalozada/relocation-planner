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
]
