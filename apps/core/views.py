from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import DocumentForm, PersonForm, ProjectForm, TaskForm
from .models import Document, Person, Project, Task


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

    def get_queryset(self):
        """Load related dashboard data for the project."""
        return Project.objects.prefetch_related("people", "documents__document_type", "documents__person", "tasks")

    def get_context_data(self, **kwargs):
        """Add dashboard counts and summaries to the template context."""
        context = super().get_context_data(**kwargs)
        project = self.object

        project_people = project.people.all()
        project_documents = project.documents.all()
        project_tasks = project.tasks.all()

        context["people_count"] = len(project_people)
        context["documents_count"] = len(project_documents)
        context["received_documents_count"] = sum(1 for document in project_documents if document.received)
        context["pending_documents_count"] = context["documents_count"] - context["received_documents_count"]
        context["tasks_count"] = len(project_tasks)
        context["completed_tasks_count"] = sum(1 for task in project_tasks if task.completed)
        context["outstanding_tasks_count"] = context["tasks_count"] - context["completed_tasks_count"]
        context["recent_people"] = sorted(project_people, key=lambda person: person.created_at, reverse=True)[:4]
        context["recent_documents"] = sorted(
            project_documents,
            key=lambda document: document.updated_at,
            reverse=True,
        )[:4]
        context["recent_tasks"] = sorted(project_tasks, key=lambda task: task.updated_at, reverse=True)[:4]
        return context


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


class DocumentListView(ListView):
    """List documents for a relocation project."""

    model = Document
    template_name = "core/document_list.html"
    context_object_name = "documents"

    def dispatch(self, request, *args, **kwargs):
        """Store the parent project for this document view."""
        self.project = get_object_or_404(Project, pk=kwargs["project_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return documents for the current project."""
        return self.project.documents.select_related("document_type", "person").order_by(
            "document_type__name",
            "person__last_name",
            "person__first_name",
        ).filter(Q(person__isnull=True) | Q(person__project=F("project")))

    def get_context_data(self, **kwargs):
        """Add the parent project to the template context."""
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context


class DocumentDetailView(DetailView):
    """Show details for a project document."""

    model = Document
    template_name = "core/document_detail.html"
    context_object_name = "document"

    def get_queryset(self):
        """Return documents with related display data."""
        return Document.objects.select_related("project", "person", "document_type").filter(
            Q(person__isnull=True) | Q(person__project=F("project")),
        )


class DocumentCreateView(SuccessMessageMixin, CreateView):
    """Create a project document."""

    model = Document
    form_class = DocumentForm
    template_name = "core/document_form.html"
    success_message = "Document added successfully."

    def dispatch(self, request, *args, **kwargs):
        """Store the parent project for this document view."""
        self.project = get_object_or_404(Project, pk=kwargs["project_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Pass the parent project to the document form."""
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.project
        return kwargs

    def form_valid(self, form):
        """Attach the new document to the parent project."""
        form.instance.project = self.project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add the parent project to the template context."""
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context

    def get_success_url(self):
        """Return the document detail URL after a successful create."""
        return reverse_lazy("core:document-detail", kwargs={"pk": self.object.pk})


class DocumentUpdateView(SuccessMessageMixin, UpdateView):
    """Update a project document."""

    model = Document
    form_class = DocumentForm
    template_name = "core/document_form.html"
    success_message = "Document updated successfully."

    def get_queryset(self):
        """Return documents with project relationships loaded."""
        return Document.objects.select_related("project", "person", "document_type").filter(
            Q(person__isnull=True) | Q(person__project=F("project")),
        )

    def get_form_kwargs(self):
        """Pass the document project to the document form."""
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.object.project
        return kwargs

    def get_context_data(self, **kwargs):
        """Add the parent project to the template context."""
        context = super().get_context_data(**kwargs)
        context["project"] = self.object.project
        return context

    def get_success_url(self):
        """Return the document detail URL after a successful update."""
        return reverse_lazy("core:document-detail", kwargs={"pk": self.object.pk})


class DocumentDeleteView(DeleteView):
    """Delete a project document."""

    model = Document
    template_name = "core/document_confirm_delete.html"
    context_object_name = "document"

    def get_queryset(self):
        """Return documents with project relationships loaded."""
        return Document.objects.select_related("project", "person", "document_type").filter(
            Q(person__isnull=True) | Q(person__project=F("project")),
        )

    def get_success_url(self):
        """Return the project documents URL after a successful delete."""
        return reverse_lazy(
            "core:document-list",
            kwargs={"project_pk": self.object.project.pk},
        )

    def form_valid(self, form):
        """Show a success message after deleting the document."""
        messages.success(self.request, "Document deleted successfully.")
        return super().form_valid(form)


class TaskListView(ListView):
    """List tasks for a relocation project."""

    model = Task
    template_name = "core/task_list.html"
    context_object_name = "tasks"

    def dispatch(self, request, *args, **kwargs):
        """Store the parent project for this task view."""
        self.project = get_object_or_404(Project, pk=kwargs["project_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return tasks for the current project."""
        return self.project.tasks.order_by("completed", "title")

    def get_context_data(self, **kwargs):
        """Add the parent project to the template context."""
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context


class TaskDetailView(DetailView):
    """Show details for a project task."""

    model = Task
    template_name = "core/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        """Return tasks with their projects loaded."""
        return Task.objects.select_related("project")


class TaskCreateView(SuccessMessageMixin, CreateView):
    """Create a project task."""

    model = Task
    form_class = TaskForm
    template_name = "core/task_form.html"
    success_message = "Task added successfully."

    def dispatch(self, request, *args, **kwargs):
        """Store the parent project for this task view."""
        self.project = get_object_or_404(Project, pk=kwargs["project_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Attach the new task to the parent project."""
        form.instance.project = self.project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add the parent project to the template context."""
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context

    def get_success_url(self):
        """Return the task detail URL after a successful create."""
        return reverse_lazy("core:task-detail", kwargs={"pk": self.object.pk})


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    """Update a project task."""

    model = Task
    form_class = TaskForm
    template_name = "core/task_form.html"
    success_message = "Task updated successfully."

    def get_queryset(self):
        """Return tasks with their projects loaded."""
        return Task.objects.select_related("project")

    def get_context_data(self, **kwargs):
        """Add the parent project to the template context."""
        context = super().get_context_data(**kwargs)
        context["project"] = self.object.project
        return context

    def get_success_url(self):
        """Return the task detail URL after a successful update."""
        return reverse_lazy("core:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(DeleteView):
    """Delete a project task."""

    model = Task
    template_name = "core/task_confirm_delete.html"
    context_object_name = "task"

    def get_queryset(self):
        """Return tasks with their projects loaded."""
        return Task.objects.select_related("project")

    def get_success_url(self):
        """Return the project tasks URL after a successful delete."""
        return reverse_lazy(
            "core:task-list",
            kwargs={"project_pk": self.object.project.pk},
        )

    def form_valid(self, form):
        """Show a success message after deleting the task."""
        messages.success(self.request, "Task deleted successfully.")
        return super().form_valid(form)
