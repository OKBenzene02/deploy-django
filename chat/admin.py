from django.contrib import admin
from .models import UploadedPDF

@admin.register(UploadedPDF)
class UploadedPDFAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    search_fields = ('file',)
    ordering = ('-uploaded_at',)

# Alternatively, you can register without a custom admin class
# admin.site.register(UploadedPDF)