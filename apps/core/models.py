from django.db import models


class Project(models.Model):
    """A relocation project that groups tasks, documents, and other resources."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the project name for the Django admin and shell."""
        return self.name


class Task(models.Model):
    """A task that belongs to a relocation project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the task title for the Django admin and shell."""
        return self.title


class Document(models.Model):
    """A document required for a relocation project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    person = models.ForeignKey(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    received = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the document name for the Django admin and shell."""
        return self.name


class Person(models.Model):
    """A person participating in a relocation project."""

    class Relationship(models.TextChoices):
        SELF = "SELF", "Self"
        SPOUSE = "SPOUSE", "Spouse"
        CHILD = "CHILD", "Child"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="people",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=20, choices=Relationship.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the person's full name for the Django admin and shell."""
        return f"{self.first_name} {self.last_name}"
