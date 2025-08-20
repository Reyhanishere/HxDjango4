from django.contrib import admin

from .models import MedicalConcept, TermVariant, UnmappedTerm, MedicalSubject

class MedicalConceptInline(admin.TabularInline):
    model= MedicalConcept.subject.through
    extra=1
    show_change_link = True
@admin.register(MedicalSubject)
class MedicalSubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_count']
    inlines=[MedicalConceptInline]
    def get_count(self, obj):
        return MedicalConcept.objects.filter(subject=obj).count()
    get_count.short_description = 'Number of Concepts'

@admin.register(TermVariant)
class TermVariantAdmin(admin.ModelAdmin):
    list_display = ['get_text', 'get_concept']
    search_fields = ['text']

    def get_concept(self, obj):
        return obj.concept.name
    def get_text(self, obj):
        return obj.text
    get_concept.short_description = "Concept"

class TermVariantInline(admin.TabularInline):   # or admin.StackedInline
    model = TermVariant
    extra = 1   # how many empty rows to show by default
    # fields = ["text", 'term_type']
    fields = ["text"]
    show_change_link = True

@admin.register(MedicalConcept)
class MedicalConceptAdmin(admin.ModelAdmin):
    list_display = ["name", "get_subject", "code"]
    
    search_fields = ["name", "get_subject", "code"]

    def get_subject(self, obj):
        return ", ".join(c.name for c in obj.subject.all())
    
    get_subject.short_description = "Subjects"

    inlines = [TermVariantInline]



@admin.register(UnmappedTerm)
class UnmappedTermAdmin(admin.ModelAdmin):
    list_display = ['text', 'concept','common_similarity', 'first_seen', 'last_seen', 'seen_count']
    search_fields = ['text']
    actions = ['assign_to_concept']

    def assign_to_concept(self, request, queryset):
        # You can replace this with a form in future for better UX
        for term in queryset:
            if term.concept:
                TermVariant.objects.create(text=term.text, concept=term.concept)
                term.delete()

        self.message_user(request, "Selected terms assigned to their concepts.")
    assign_to_concept.short_description = "Assign to its concept"