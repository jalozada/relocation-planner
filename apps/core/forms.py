from django import forms

from .models import Person, Project


class ProjectForm(forms.ModelForm):
    """Form for creating and updating relocation projects."""

    class Meta:
        model = Project
        fields = ["name", "description"]


class PersonForm(forms.ModelForm):
    """Form for creating and updating project participants."""

    class Meta:
        model = Person
        fields = ["first_name", "last_name", "relationship"]
