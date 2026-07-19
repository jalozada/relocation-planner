from .models import Document, RelocationTemplate, Task


def apply_relocation_template(project, template: RelocationTemplate) -> None:
    """Create project documents and tasks from a relocation template."""
    documents = [
        Document(
            project=project,
            document_type=document_item.document_type,
            description=document_item.description,
        )
        for document_item in template.document_items.select_related("document_type")
    ]
    if documents:
        Document.objects.bulk_create(documents)

    tasks = [
        Task(
            project=project,
            title=task_item.title,
            description=task_item.description,
        )
        for task_item in template.task_items.all()
    ]
    if tasks:
        Task.objects.bulk_create(tasks)
