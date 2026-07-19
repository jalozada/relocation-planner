from django.db import migrations


TEMPLATE_NAME = "Standard Relocation"

DOCUMENT_TYPE_NAMES = [
    "Passport",
    "Birth Certificate",
    "Marriage Certificate",
    "Driver License",
    "School Transcript",
    "Visa",
    "Medical Records",
    "Vaccination Record",
]

TASKS = [
    ("Review required documents", "Confirm which documents are needed for each person."),
    ("Confirm travel timeline", "Capture major relocation dates and travel milestones."),
    ("Gather school records", "Collect transcripts or school records when applicable."),
    ("Review medical records", "Identify medical and vaccination records to request."),
    ("Track visa requirements", "Review visa requirements and related deadlines."),
]


def seed_relocation_templates(apps, schema_editor):
    """Create the default relocation template and reusable items."""
    DocumentType = apps.get_model("core", "DocumentType")
    RelocationTemplate = apps.get_model("core", "RelocationTemplate")
    RelocationTemplateDocument = apps.get_model("core", "RelocationTemplateDocument")
    RelocationTemplateTask = apps.get_model("core", "RelocationTemplateTask")

    template, _created = RelocationTemplate.objects.get_or_create(
        name=TEMPLATE_NAME,
        defaults={
            "description": "A practical starter checklist for a general relocation.",
            "active": True,
        },
    )

    document_types = DocumentType.objects.filter(name__in=DOCUMENT_TYPE_NAMES, active=True)
    for document_type in document_types:
        RelocationTemplateDocument.objects.get_or_create(
            template=template,
            document_type=document_type,
            defaults={"description": document_type.description},
        )

    for title, description in TASKS:
        RelocationTemplateTask.objects.get_or_create(
            template=template,
            title=title,
            defaults={"description": description},
        )


def remove_relocation_templates(apps, schema_editor):
    """Remove the default relocation template."""
    RelocationTemplate = apps.get_model("core", "RelocationTemplate")
    RelocationTemplate.objects.filter(name=TEMPLATE_NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_relocation_templates"),
    ]

    operations = [
        migrations.RunPython(seed_relocation_templates, remove_relocation_templates),
    ]
