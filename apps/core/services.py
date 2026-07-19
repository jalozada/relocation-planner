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


def build_project_dashboard_context(project) -> dict:
    """Return dashboard counts and summaries for a project."""
    project_people = project.people.all()
    project_documents = project.documents.all()
    project_tasks = project.tasks.all()
    project_milestones = project.milestones.all()

    documents_count = len(project_documents)
    received_documents_count = sum(1 for document in project_documents if document.received)
    tasks_count = len(project_tasks)
    completed_tasks_count = sum(1 for task in project_tasks if task.completed)
    milestones_count = len(project_milestones)
    completed_milestones_count = sum(1 for milestone in project_milestones if milestone.completed)

    return {
        "people_count": len(project_people),
        "documents_count": documents_count,
        "received_documents_count": received_documents_count,
        "pending_documents_count": documents_count - received_documents_count,
        "tasks_count": tasks_count,
        "completed_tasks_count": completed_tasks_count,
        "outstanding_tasks_count": tasks_count - completed_tasks_count,
        "milestones_count": milestones_count,
        "completed_milestones_count": completed_milestones_count,
        "outstanding_milestones_count": milestones_count - completed_milestones_count,
        "recent_people": sorted(project_people, key=lambda person: person.created_at, reverse=True)[:4],
        "recent_documents": sorted(
            project_documents,
            key=lambda document: document.updated_at,
            reverse=True,
        )[:4],
        "recent_tasks": sorted(project_tasks, key=lambda task: task.updated_at, reverse=True)[:4],
        "recent_milestones": sorted(
            project_milestones,
            key=lambda milestone: (milestone.target_date is None, milestone.target_date, milestone.title),
        )[:4],
    }
