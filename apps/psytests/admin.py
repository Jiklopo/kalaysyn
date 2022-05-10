from django.contrib import admin

from apps.psytests.models import PsyTest, Question, Variant


class VariantInline(admin.TabularInline):
    model = Variant


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(PsyTest)
class PsyTestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    exclude = ['ratings_received']
    readonly_fields = ['rating']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['test']
    search_fields = ['text']
    inlines = [VariantInline]
