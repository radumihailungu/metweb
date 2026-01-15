from django.contrib import admin
from django.utils.html import format_html

from .models import ArtObject
from .admin_forms import ArtObjectAdminForm

@admin.register(ArtObject)
class ArtObjectAdmin(admin.ModelAdmin):
    form = ArtObjectAdminForm

    list_display = ("id", "title_col", "artist_col", "department_col", "image_preview")
    search_fields = ("data__title", "data__artistDisplayName", "data__department", "data__classification")
    list_per_page = 25

    fieldsets = (
        ("Informații principale", {
            "fields": ("title", "artistDisplayName", "department", "classification", "culture")
        }),
        ("Detalii obiect", {
            "fields": ("objectName", "objectDate", "medium")
        }),
        ("Locație", {
            "fields": ("country", "region", "city")
        }),
        ("Linkuri / credit", {
            "fields": ("creditLine", "objectURL")
        }),
        ("Imagine", {
            "fields": ("image",)
        }),
    )

    #extragere date din json
    def title_col(self, obj):
        return (obj.data or {}).get("title", "")
    title_col.short_description = "Title"

    def artist_col(self, obj):
        return (obj.data or {}).get("artistDisplayName", "")
    artist_col.short_description = "Artist"

    def department_col(self, obj):
        return (obj.data or {}).get("department", "")
    department_col.short_description = "Department"

    def image_preview(self, obj):
        img = (obj.data or {}).get("image", "")
        if img:
            return format_html('<img src="{}" style="max-height:60px;"/>', img)
        return "-"
    image_preview.short_description = "Image"
