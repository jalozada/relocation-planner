from django import forms

from .models import Document, DocumentType, Person, Project, RelocationTemplate, Task


class ProjectForm(forms.ModelForm):
    """Form for creating and updating relocation projects."""

    relocation_template = forms.ModelChoiceField(
        queryset=RelocationTemplate.objects.none(),
        required=False,
        help_text="Optionally start with default documents and tasks.",
    )

    class Meta:
        model = Project
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields.pop("relocation_template")
            return

        self.fields["relocation_template"].queryset = RelocationTemplate.objects.filter(
            active=True,
        ).order_by("name")


class PersonForm(forms.ModelForm):
    """Form for creating and updating project participants."""

    class Meta:
        model = Person
        fields = ["first_name", "last_name", "relationship"]


class DocumentForm(forms.ModelForm):
    """Form for creating and updating project documents."""

    class Meta:
        model = Document
        fields = ["document_type", "person", "description", "received"]

    def __init__(self, *args, project, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["person"].queryset = project.people.order_by("last_name", "first_name")
        self.fields["person"].required = False

        document_type_queryset = DocumentType.objects.filter(active=True)
        if self.instance.pk and self.instance.document_type_id:
            document_type_queryset = DocumentType.objects.filter(
                pk=self.instance.document_type_id,
            ) | document_type_queryset

        self.fields["document_type"].queryset = document_type_queryset.distinct().order_by("name")


class TaskForm(forms.ModelForm):
    """Form for creating and updating project tasks."""

    class Meta:
        model = Task
        fields = ["title", "description", "completed"]
