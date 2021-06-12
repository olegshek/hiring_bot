from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from core.forms import TextForm


class TextAdmin(TranslationAdmin):
    form = TextForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
