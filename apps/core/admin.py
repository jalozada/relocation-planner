from django.contrib import admin

from .models import DocumentType, RelocationTemplate, RelocationTemplateDocument, RelocationTemplateTask


admin.site.register(DocumentType)


class RelocationTemplateDocumentInline(admin.TabularInline):
    model = RelocationTemplateDocument
    extra = 0


class RelocationTemplateTaskInline(admin.TabularInline):
    model = RelocationTemplateTask
    extra = 0


@admin.register(RelocationTemplate)
class RelocationTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "updated_at"]
    list_filter = ["active"]
    search_fields = ["name", "description"]
    inlines = [RelocationTemplateDocumentInline, RelocationTemplateTaskInline]
