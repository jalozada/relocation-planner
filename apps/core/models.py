from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    """A relocation project that groups tasks, documents, and other resources."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the project name for the Django admin and shell."""
        return self.name

class Workstream(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="workstreams",
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=30, default="blue")
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]
        unique_together = ("project", "slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Task(models.Model):
    """A task that belongs to a relocation project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    milestone = models.ForeignKey(
        "Milestone",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
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


class Milestone(models.Model):
    """A project milestone for tracking major relocation phases."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="milestones",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the milestone title for the Django admin and shell."""
        return self.title


class DocumentType(models.Model):
    """A reusable type for standardizing relocation document names."""

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the document type name for the Django admin and shell."""
        return self.name


class RelocationTemplate(models.Model):
    """A reusable starting point for relocation projects."""

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the template name for the Django admin and shell."""
        return self.name


class RelocationTemplateDocument(models.Model):
    """A default document requirement in a relocation template."""

    template = models.ForeignKey(
        RelocationTemplate,
        on_delete=models.CASCADE,
        related_name="document_items",
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        related_name="template_document_items",
    )
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        """Return the template document type name."""
        return str(self.document_type)


class RelocationTemplateTask(models.Model):
    """A default task in a relocation template."""

    template = models.ForeignKey(
        RelocationTemplate,
        on_delete=models.CASCADE,
        related_name="task_items",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        """Return the template task title."""
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
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        related_name="documents",
    )
    description = models.TextField(blank=True)
    received = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the document name for the Django admin and shell."""
        if self.person:
            return f"{self.document_type} ({self.person})"
        return str(self.document_type)


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
