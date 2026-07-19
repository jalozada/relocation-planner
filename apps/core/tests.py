from django.test import TestCase
from django.urls import reverse

from .models import Person, Project


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
