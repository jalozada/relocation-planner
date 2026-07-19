from django.db import migrations


DOCUMENT_TYPES = [
    "Passport",
    "Birth Certificate",
    "Marriage Certificate",
    "Driver License",
    "School Transcript",
    "DD-214",
    "Visa",
    "Medical Records",
    "Vaccination Record",
]


def seed_document_types(apps, schema_editor):
    """Create standard document types and backfill existing documents."""
    Document = apps.get_model("core", "Document")
    DocumentType = apps.get_model("core", "DocumentType")

    document_types = {}
    for name in DOCUMENT_TYPES:
        document_type, _created = DocumentType.objects.get_or_create(name=name)
        document_types[name] = document_type

    for document in Document.objects.all():
        document_type = document_types.get(document.name)
        if document_type is None:
            document_type, _created = DocumentType.objects.get_or_create(name=document.name)
            document_types[document.name] = document_type

        document.document_type = document_type
        document.save(update_fields=["document_type"])


def remove_seed_document_types(apps, schema_editor):
    """Remove document types inserted by this migration when unused."""
    DocumentType = apps.get_model("core", "DocumentType")
    DocumentType.objects.filter(name__in=DOCUMENT_TYPES, documents__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_documenttype_document_document_type"),
    ]

    operations = [
        migrations.RunPython(seed_document_types, remove_seed_document_types),
    ]
