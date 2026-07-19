from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PersonForm, ProjectForm
from .models import Person, Project


def home(request):
    """Render the application home page."""
    return render(request, "home.html")


class ProjectListView(ListView):
    """List relocation projects."""

    model = Project
    template_name = "core/project_list.html"
    context_object_name = "projects"
    ordering = ["name"]


class ProjectDetailView(DetailView):
    """Show details for a relocation project."""

    model = Project
    template_name = "core/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(SuccessMessageMixin, CreateView):
    """Create a relocation project."""

    model = Project
    form_class = ProjectForm
    template_name = "core/project_form.html"
    success_url = reverse_lazy("core:project-list")
    success_message = "Project created successfully."


class ProjectUpdateView(SuccessMessageMixin, UpdateView):
    """Update a relocation project."""

    model = Project
    form_class = ProjectForm
    template_name = "core/project_form.html"
    success_message = "Project updated successfully."

    def get_success_url(self):
        """Return the project detail URL after a successful update."""
        return reverse_lazy("core:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(DeleteView):
    """Delete a relocation project."""

    model = Project
    template_name = "core/project_confirm_delete.html"
    context_object_name = "project"
    success_url = reverse_lazy("core:project-list")

    def form_valid(self, form):
        """Show a success message after deleting the project."""
        messages.success(self.request, "Project deleted successfully.")
        return super().form_valid(form)


class PersonListView(ListView):
    """List people for a relocation project."""

    model = Person
    template_name = "core/person_list.html"
    context_object_name = "people"

    def dispatch(self, request, *args, **kwargs):
        """Store the parent project for this people view."""
        self.project = get_object_or_404(Project, pk=kwargs["project_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return people for the current project."""
        return self.project.people.order_by("last_name", "first_name")

    def get_context_data(self, **kwargs):
        """Add the parent project to the template context."""
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context


class PersonDetailView(DetailView):
    """Show details for a project participant."""

    model = Person
    template_name = "core/person_detail.html"
    context_object_name = "person"


class PersonCreateView(SuccessMessageMixin, CreateView):
    """Create a project participant."""

    model = Person
    form_class = PersonForm
    template_name = "core/person_form.html"
    success_message = "Person added successfully."

    def dispatch(self, request, *args, **kwargs):
        """Store the parent project for this people view."""
        self.project = get_object_or_404(Project, pk=kwargs["project_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Attach the new person to the parent project."""
        form.instance.project = self.project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add the parent project to the template context."""
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context

    def get_success_url(self):
        """Return the person detail URL after a successful create."""
        return reverse_lazy("core:person-detail", kwargs={"pk": self.object.pk})


class PersonUpdateView(SuccessMessageMixin, UpdateView):
    """Update a project participant."""

    model = Person
    form_class = PersonForm
    template_name = "core/person_form.html"
    success_message = "Person updated successfully."

    def get_success_url(self):
        """Return the person detail URL after a successful update."""
        return reverse_lazy("core:person-detail", kwargs={"pk": self.object.pk})


class PersonDeleteView(DeleteView):
    """Delete a project participant."""

    model = Person
    template_name = "core/person_confirm_delete.html"
    context_object_name = "person"

    def get_success_url(self):
        """Return the project people URL after a successful delete."""
        return reverse_lazy(
            "core:person-list",
            kwargs={"project_pk": self.object.project.pk},
        )

    def form_valid(self, form):
        """Show a success message after deleting the person."""
        messages.success(self.request, "Person deleted successfully.")
        return super().form_valid(form)
