from django.test import TestCase
from django.urls import reverse

from .forms import DocumentForm, ProjectForm
from .models import Document, DocumentType, Person, Project, RelocationTemplate, Task
from .services import apply_relocation_template


class ProjectCRUDTests(TestCase):
    """Tests for project CRUD views."""

    def test_project_list_returns_http_200(self):
        """The project list page loads successfully."""
        response = self.client.get(reverse("core:project-list"))

        self.assertEqual(response.status_code, 200)

    def test_project_create_succeeds(self):
        """A project can be created through the create view."""
        response = self.client.post(
            reverse("core:project-create"),
            {
                "name": "Move planning",
                "description": "Initial planning notes.",
            },
        )

        self.assertRedirects(response, reverse("core:project-list"))
        self.assertTrue(Project.objects.filter(name="Move planning").exists())

    def test_project_update_succeeds(self):
        """A project can be updated through the update view."""
        project = Project.objects.create(name="Old name", description="Old notes.")

        response = self.client.post(
            reverse("core:project-update", kwargs={"pk": project.pk}),
            {
                "name": "New name",
                "description": "Updated notes.",
            },
        )

        self.assertRedirects(response, reverse("core:project-detail", kwargs={"pk": project.pk}))
        project.refresh_from_db()
        self.assertEqual(project.name, "New name")
        self.assertEqual(project.description, "Updated notes.")

    def test_project_delete_succeeds(self):
        """A project can be deleted through the delete view."""
        project = Project.objects.create(name="Project to delete")

        response = self.client.post(reverse("core:project-delete", kwargs={"pk": project.pk}))

        self.assertRedirects(response, reverse("core:project-list"))
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())


class PersonCRUDTests(TestCase):
    """Tests for person CRUD views."""

    def test_person_list_per_project_returns_http_200(self):
        """The per-project person list page loads successfully."""
        project = Project.objects.create(name="People project")

        response = self.client.get(reverse("core:person-list", kwargs={"project_pk": project.pk}))

        self.assertEqual(response.status_code, 200)

    def test_person_create_assigns_project_from_url(self):
        """Creating a person assigns the project from the nested URL."""
        project = Project.objects.create(name="People project")

        response = self.client.post(
            reverse("core:person-create", kwargs={"project_pk": project.pk}),
            {
                "first_name": "First",
                "last_name": "Person",
                "relationship": Person.Relationship.SELF,
            },
        )

        person = Person.objects.get(first_name="First", last_name="Person")
        self.assertRedirects(response, reverse("core:person-detail", kwargs={"pk": person.pk}))
        self.assertEqual(person.project, project)

    def test_person_update_succeeds(self):
        """A person can be updated through the update view."""
        project = Project.objects.create(name="People project")
        person = Person.objects.create(
            project=project,
            first_name="Old",
            last_name="Name",
            relationship=Person.Relationship.SELF,
        )

        response = self.client.post(
            reverse("core:person-update", kwargs={"pk": person.pk}),
            {
                "first_name": "New",
                "last_name": "Name",
                "relationship": Person.Relationship.SPOUSE,
            },
        )

        self.assertRedirects(response, reverse("core:person-detail", kwargs={"pk": person.pk}))
        person.refresh_from_db()
        self.assertEqual(person.first_name, "New")
        self.assertEqual(person.relationship, Person.Relationship.SPOUSE)

    def test_person_delete_succeeds(self):
        """A person can be deleted through the delete view."""
        project = Project.objects.create(name="People project")
        person = Person.objects.create(
            project=project,
            first_name="Delete",
            last_name="Person",
            relationship=Person.Relationship.CHILD,
        )

        response = self.client.post(reverse("core:person-delete", kwargs={"pk": person.pk}))

        self.assertRedirects(response, reverse("core:person-list", kwargs={"project_pk": project.pk}))
        self.assertFalse(Person.objects.filter(pk=person.pk).exists())


class ProjectDashboardTests(TestCase):
    """Tests for project dashboard summaries."""

    def test_project_dashboard_shows_counts(self):
        """The dashboard displays people, document, and task counts."""
        project = Project.objects.create(name="Dashboard project")
        document_type = DocumentType.objects.get(name="Passport")
        Person.objects.create(
            project=project,
            first_name="First",
            last_name="Person",
            relationship=Person.Relationship.SELF,
        )
        Document.objects.create(project=project, document_type=document_type, received=True)
        Document.objects.create(project=project, document_type=document_type, received=False)
        Task.objects.create(project=project, title="Complete task", completed=True)
        Task.objects.create(project=project, title="Open task", completed=False)

        response = self.client.get(reverse("core:project-detail", kwargs={"pk": project.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["people_count"], 1)
        self.assertEqual(response.context["documents_count"], 2)
        self.assertEqual(response.context["received_documents_count"], 1)
        self.assertEqual(response.context["pending_documents_count"], 1)
        self.assertEqual(response.context["tasks_count"], 2)
        self.assertEqual(response.context["completed_tasks_count"], 1)
        self.assertEqual(response.context["outstanding_tasks_count"], 1)


class DocumentCRUDTests(TestCase):
    """Tests for document CRUD views and scoped form choices."""

    def test_document_list_returns_http_200(self):
        """The per-project document list page loads successfully."""
        project = Project.objects.create(name="Document project")

        response = self.client.get(reverse("core:document-list", kwargs={"project_pk": project.pk}))

        self.assertEqual(response.status_code, 200)

    def test_document_detail_returns_http_200(self):
        """The document detail page loads successfully."""
        project = Project.objects.create(name="Document project")
        document_type = DocumentType.objects.get(name="Passport")
        document = Document.objects.create(project=project, document_type=document_type)

        response = self.client.get(reverse("core:document-detail", kwargs={"pk": document.pk}))

        self.assertEqual(response.status_code, 200)

    def test_document_create_assigns_project_from_url(self):
        """Creating a document assigns the project from the nested URL."""
        project = Project.objects.create(name="Document project")
        document_type = DocumentType.objects.get(name="Passport")
        person = Person.objects.create(
            project=project,
            first_name="First",
            last_name="Person",
            relationship=Person.Relationship.SELF,
        )

        response = self.client.post(
            reverse("core:document-create", kwargs={"project_pk": project.pk}),
            {
                "document_type": document_type.pk,
                "person": person.pk,
                "description": "Passport notes.",
                "received": "on",
            },
        )

        document = Document.objects.get(description="Passport notes.")
        self.assertRedirects(response, reverse("core:document-detail", kwargs={"pk": document.pk}))
        self.assertEqual(document.project, project)
        self.assertEqual(document.person, person)
        self.assertTrue(document.received)

    def test_project_level_document_can_be_created_without_person(self):
        """Documents can be created without assigning a person."""
        project = Project.objects.create(name="Document project")
        document_type = DocumentType.objects.get(name="Marriage Certificate")

        response = self.client.post(
            reverse("core:document-create", kwargs={"project_pk": project.pk}),
            {
                "document_type": document_type.pk,
                "person": "",
                "description": "Project-level document.",
            },
        )

        document = Document.objects.get(description="Project-level document.")
        self.assertRedirects(response, reverse("core:document-detail", kwargs={"pk": document.pk}))
        self.assertIsNone(document.person)

    def test_document_update_succeeds(self):
        """A document can be updated through the update view."""
        project = Project.objects.create(name="Document project")
        document_type = DocumentType.objects.get(name="Passport")
        document = Document.objects.create(project=project, document_type=document_type)

        response = self.client.post(
            reverse("core:document-update", kwargs={"pk": document.pk}),
            {
                "document_type": document_type.pk,
                "person": "",
                "description": "Updated document notes.",
                "received": "on",
            },
        )

        self.assertRedirects(response, reverse("core:document-detail", kwargs={"pk": document.pk}))
        document.refresh_from_db()
        self.assertEqual(document.description, "Updated document notes.")
        self.assertTrue(document.received)

    def test_document_delete_succeeds(self):
        """A document can be deleted through the delete view."""
        project = Project.objects.create(name="Document project")
        document_type = DocumentType.objects.get(name="Passport")
        document = Document.objects.create(project=project, document_type=document_type)

        response = self.client.post(reverse("core:document-delete", kwargs={"pk": document.pk}))

        self.assertRedirects(response, reverse("core:document-list", kwargs={"project_pk": project.pk}))
        self.assertFalse(Document.objects.filter(pk=document.pk).exists())

    def test_document_person_choices_are_filtered_by_project(self):
        """Document forms only offer people from the current project."""
        project = Project.objects.create(name="Document project")
        other_project = Project.objects.create(name="Other project")
        project_person = Person.objects.create(
            project=project,
            first_name="Project",
            last_name="Person",
            relationship=Person.Relationship.SELF,
        )
        other_person = Person.objects.create(
            project=other_project,
            first_name="Other",
            last_name="Person",
            relationship=Person.Relationship.SELF,
        )

        form = DocumentForm(project=project)

        self.assertIn(project_person, form.fields["person"].queryset)
        self.assertNotIn(other_person, form.fields["person"].queryset)

    def test_document_type_choices_are_active_on_create(self):
        """Document create forms only offer active document types."""
        project = Project.objects.create(name="Document project")
        active_type = DocumentType.objects.get(name="Passport")
        inactive_type = DocumentType.objects.create(name="Archived Type", active=False)

        form = DocumentForm(project=project)

        self.assertIn(active_type, form.fields["document_type"].queryset)
        self.assertNotIn(inactive_type, form.fields["document_type"].queryset)

    def test_document_update_includes_current_inactive_document_type(self):
        """Document update forms include the current type even when inactive."""
        project = Project.objects.create(name="Document project")
        inactive_type = DocumentType.objects.create(name="Archived Type", active=False)
        document = Document.objects.create(project=project, document_type=inactive_type)

        form = DocumentForm(project=project, instance=document)

        self.assertIn(inactive_type, form.fields["document_type"].queryset)

    def test_document_update_rejects_switching_to_other_inactive_document_type(self):
        """Document updates cannot switch to another inactive document type."""
        project = Project.objects.create(name="Document project")
        current_type = DocumentType.objects.create(name="Current Archived Type", active=False)
        other_inactive_type = DocumentType.objects.create(name="Other Archived Type", active=False)
        document = Document.objects.create(project=project, document_type=current_type)

        response = self.client.post(
            reverse("core:document-update", kwargs={"pk": document.pk}),
            {
                "document_type": other_inactive_type.pk,
                "person": "",
                "description": "Invalid update.",
            },
        )

        self.assertEqual(response.status_code, 200)
        document.refresh_from_db()
        self.assertEqual(document.document_type, current_type)

    def test_cross_project_document_person_assignment_is_rejected(self):
        """Document create rejects a person from another project."""
        project = Project.objects.create(name="Document project")
        other_project = Project.objects.create(name="Other project")
        document_type = DocumentType.objects.get(name="Passport")
        other_person = Person.objects.create(
            project=other_project,
            first_name="Other",
            last_name="Person",
            relationship=Person.Relationship.SELF,
        )

        response = self.client.post(
            reverse("core:document-create", kwargs={"project_pk": project.pk}),
            {
                "document_type": document_type.pk,
                "person": other_person.pk,
                "description": "Invalid person.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Document.objects.filter(description="Invalid person.").exists())


class TaskCRUDTests(TestCase):
    """Tests for task CRUD views."""

    def test_task_list_returns_http_200(self):
        """The per-project task list page loads successfully."""
        project = Project.objects.create(name="Task project")

        response = self.client.get(reverse("core:task-list", kwargs={"project_pk": project.pk}))

        self.assertEqual(response.status_code, 200)

    def test_task_detail_returns_http_200(self):
        """The task detail page loads successfully."""
        project = Project.objects.create(name="Task project")
        task = Task.objects.create(project=project, title="Gather paperwork")

        response = self.client.get(reverse("core:task-detail", kwargs={"pk": task.pk}))

        self.assertEqual(response.status_code, 200)

    def test_task_create_assigns_project_from_url(self):
        """Creating a task assigns the project from the nested URL."""
        project = Project.objects.create(name="Task project")

        response = self.client.post(
            reverse("core:task-create", kwargs={"project_pk": project.pk}),
            {
                "title": "Gather paperwork",
                "description": "Find the folder.",
            },
        )

        task = Task.objects.get(title="Gather paperwork")
        self.assertRedirects(response, reverse("core:task-detail", kwargs={"pk": task.pk}))
        self.assertEqual(task.project, project)
        self.assertFalse(task.completed)

    def test_task_update_succeeds(self):
        """A task can be updated through the update view."""
        project = Project.objects.create(name="Task project")
        task = Task.objects.create(project=project, title="Old task")

        response = self.client.post(
            reverse("core:task-update", kwargs={"pk": task.pk}),
            {
                "title": "Updated task",
                "description": "Updated notes.",
                "completed": "on",
            },
        )

        self.assertRedirects(response, reverse("core:task-detail", kwargs={"pk": task.pk}))
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated task")
        self.assertEqual(task.description, "Updated notes.")
        self.assertTrue(task.completed)

    def test_task_delete_succeeds(self):
        """A task can be deleted through the delete view."""
        project = Project.objects.create(name="Task project")
        task = Task.objects.create(project=project, title="Delete task")

        response = self.client.post(reverse("core:task-delete", kwargs={"pk": task.pk}))

        self.assertRedirects(response, reverse("core:task-list", kwargs={"project_pk": project.pk}))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_task_update_ignores_manipulated_project_assignment(self):
        """Task update does not allow project reassignment through form data."""
        project = Project.objects.create(name="Task project")
        other_project = Project.objects.create(name="Other project")
        task = Task.objects.create(project=project, title="Scoped task")

        response = self.client.post(
            reverse("core:task-update", kwargs={"pk": task.pk}),
            {
                "project": other_project.pk,
                "title": "Still scoped",
                "description": "",
            },
        )

        self.assertRedirects(response, reverse("core:task-detail", kwargs={"pk": task.pk}))
        task.refresh_from_db()
        self.assertEqual(task.project, project)


class RelocationTemplateTests(TestCase):
    """Tests for creating projects from relocation templates."""

    def test_apply_relocation_template_creates_project_level_documents(self):
        """Applying a template creates project-level pending documents."""
        project = Project.objects.create(name="Template project")
        template = RelocationTemplate.objects.get(name="Standard Relocation")

        apply_relocation_template(project, template)

        self.assertGreater(project.documents.count(), 0)
        self.assertTrue(project.documents.filter(person__isnull=True, received=False).exists())

    def test_apply_relocation_template_creates_tasks(self):
        """Applying a template creates outstanding tasks."""
        project = Project.objects.create(name="Template project")
        template = RelocationTemplate.objects.get(name="Standard Relocation")

        apply_relocation_template(project, template)

        self.assertGreater(project.tasks.count(), 0)
        self.assertTrue(project.tasks.filter(completed=False).exists())

    def test_project_create_with_template_creates_documents_and_tasks(self):
        """Creating a project with a template initializes documents and tasks."""
        template = RelocationTemplate.objects.get(name="Standard Relocation")

        response = self.client.post(
            reverse("core:project-create"),
            {
                "name": "Templated project",
                "description": "Created from a template.",
                "relocation_template": template.pk,
            },
        )

        project = Project.objects.get(name="Templated project")
        self.assertRedirects(response, reverse("core:project-list"))
        self.assertGreater(project.documents.count(), 0)
        self.assertGreater(project.tasks.count(), 0)

    def test_project_create_without_template_still_succeeds(self):
        """Creating a project without a template does not create defaults."""
        response = self.client.post(
            reverse("core:project-create"),
            {
                "name": "Blank project",
                "description": "No template.",
                "relocation_template": "",
            },
        )

        project = Project.objects.get(name="Blank project")
        self.assertRedirects(response, reverse("core:project-list"))
        self.assertEqual(project.documents.count(), 0)
        self.assertEqual(project.tasks.count(), 0)

    def test_inactive_templates_are_not_offered_in_project_form(self):
        """Inactive templates are hidden from the project form."""
        inactive_template = RelocationTemplate.objects.create(name="Inactive Template", active=False)

        form = ProjectForm()

        self.assertNotIn(inactive_template, form.fields["relocation_template"].queryset)

    def test_relocation_template_field_is_removed_when_editing_project(self):
        """Project edit forms do not expose template initialization."""
        project = Project.objects.create(name="Existing project")

        form = ProjectForm(instance=project)

        self.assertNotIn("relocation_template", form.fields)

    def test_project_update_does_not_apply_template(self):
        """Updating a project ignores template data."""
        project = Project.objects.create(name="Existing project")
        template = RelocationTemplate.objects.get(name="Standard Relocation")

        response = self.client.post(
            reverse("core:project-update", kwargs={"pk": project.pk}),
            {
                "name": "Existing project updated",
                "description": "Updated.",
                "relocation_template": template.pk,
            },
        )

        self.assertRedirects(response, reverse("core:project-detail", kwargs={"pk": project.pk}))
        project.refresh_from_db()
        self.assertEqual(project.name, "Existing project updated")
        self.assertEqual(project.documents.count(), 0)
        self.assertEqual(project.tasks.count(), 0)
